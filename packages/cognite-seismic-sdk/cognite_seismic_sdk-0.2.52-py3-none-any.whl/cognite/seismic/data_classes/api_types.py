import json
import math
import os
from typing import Iterable, List, Mapping, Optional, Tuple, Union

import numpy as np
from cognite.seismic._api.utility import Direction, LineRange, MaybeString

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import CRS as CRSProto
    from cognite.seismic.protos.types_pb2 import GeoJson
    from cognite.seismic.protos.types_pb2 import Geometry as GeometryProto
    from cognite.seismic.protos.types_pb2 import IngestionSource, Wkt
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import BinaryHeader as BinaryHeaderProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import TextHeader as TextHeaderProto
    from google.protobuf.json_format import MessageToDict
else:
    from enum import Enum

    class IngestionSource(Enum):
        """Enum of ingestion sources."""

        INVALID_SOURCE = 0
        """Indicates that a source was not specified or was invalid."""
        FILE_SOURCE = 1
        """Indicates ingestion from a file"""
        TRACE_WRITER = 2
        """Indicates creation by trace writer"""


# Contains types returned by the SDK API.


class Coordinate:
    """Represents physical coordinates in a given CRS.

    Attributes:
        crs (str): The coordinate reference system of the coordinate. Generally should be an EPSG code.
        x (float): The x value of the coordinate.
        y (float): The y value of the coordinate.
    """

    crs: str
    x: float
    y: float

    def __init__(self, crs, x, y):
        self.crs = crs
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate<crs: {self.crs}, x: {self.x}, y: {self.y}>"

    @staticmethod
    def from_proto(proto) -> "Coordinate":
        return Coordinate(crs=proto.crs, x=proto.x, y=proto.y)


class Trace:
    """Represents a seismic trace with a single inline / xline coordinate.

    Attributes:
        trace_header (bytes): The raw trace header.
        inline (int): The inline number
        xline (int): The xline number
        trace (List[float]): The trace values
        coordinate (:py:class:`Coordinate`): The coordinate of the trace
    """

    trace_header: bytes
    inline: int
    xline: int
    trace: List[float]
    coordinate: Coordinate

    def __init__(self, trace_header, inline, xline, trace, coordinate):
        self.trace_header = trace_header
        self.inline = inline
        self.xline = xline
        self.trace = trace
        self.coordinate = coordinate

    def __repr__(self):
        return f"Trace<inline: {self.inline}, xline: {self.xline}, coordinates: {str(self.coordinate)}, trace: {self.trace}>"

    @staticmethod
    def from_proto(proto) -> "Trace":
        return Trace(
            trace_header=proto.trace_header,
            inline=proto.iline.value,
            xline=proto.xline.value,
            trace=proto.trace,
            coordinate=Coordinate.from_proto(proto.coordinate),
        )


class RangeInclusive:
    """Represents an inclusive range of inlines/xlines or depth coordinates.

    Attributes:
        start: The first linenumber encompassed by the range
        stop: The last linenumber encompassed by the range
        step: The distance between linenumbers"""

    start: int
    stop: int
    step: int

    def __init__(self, start: int, stop: int, step: Optional[int] = 1):
        if step == 0:
            raise ValueError("RangeInclusive(): step must be nonzero")
        self.start = start
        self.stop = start + ((stop - start) // step) * step
        self.step = step

    @classmethod
    def from_linerange(cls, linerange: LineRange) -> "RangeInclusive":
        """Construct a RangeInclusive from a (start, stop) or (start, stop, step) tuple"""
        if len(linerange) == 2:
            return cls(linerange[0], linerange[1], 1)
        elif len(linerange) == 3:
            return cls(linerange[0], linerange[1], linerange[2])
        else:
            raise ValueError("Linerange must have 2 or 3 elements")

    @classmethod
    def widest(cls, ranges: Iterable[Tuple[int, int]]) -> "RangeInclusive":
        """Finds the widest range among the (min, max) tuples in ranges, and returns the result as a RangeInclusive"""
        min_start = None
        max_stop = None
        for (start, stop) in ranges:
            if min_start is None or start < min_start:
                min_start = start
            if max_stop is None or stop > max_stop:
                max_stop = stop
        if min_start is None or max_stop is None:
            raise ValueError("Empty range")
        return RangeInclusive(min_start, max_stop)

    def index(self, line: int) -> int:
        """Compute the index of a given linenumber in this range"""
        if line < self.start or line > self.stop:
            raise ValueError(f"line {line} out of range")
        if (line - self.start) % self.step != 0:
            raise ValueError(f"line {line} incompatible with step {self.step} starting from {self.start}")
        return (line - self.start) // self.step

    def to_linerange(self) -> LineRange:
        """Return a (start, stop) or a (start, stop, step) tuple"""
        if self.step == 1:
            return (self.start, self.stop)
        else:
            return (self.start, self.stop, self.step)

    def __len__(self) -> int:
        """Return the number of lines described by this range"""
        return (self.stop - self.start) // self.step + 1

    def __iter__(self):
        cur = self.start
        while cur <= self.stop:
            yield cur
            cur += self.step

    def __contains__(self, line: int) -> bool:
        return line >= self.start and line <= self.stop and (line - self.start) % self.step == 0

    def __repr__(self):
        return f"RangeInclusive({self.start}, {self.stop}, {self.step})"

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop and self.step == other.step


class VolumeDef:
    """Represents a VolumeDef, a method to describe an inline/xline grid. Refer to :ref:`VolumeDef Overview` for more information."""

    json: str

    def __init__(self, json_payload):
        self.json = json_payload
        self.parsed = json.loads(json_payload)
        if self.parsed["version"] >= 200:
            raise Exception(
                f'The specified volumedef version {self.parsed["version"]} is not supported by this version of the Cognite SDK.'
            )
        if "direction" in self.parsed:
            if self.parsed["direction"] == "inline":
                self.direction = Direction.INLINE
            elif self.parsed["direction"] == "crossline":
                self.direction = Direction.XLINE
            else:
                raise Exception(f'Unknown direction "{direction}"')
        else:
            self.direction = Direction.INLINE

    def __repr__(self):
        return f"VolumeDef<{self.json}>"

    @staticmethod
    def from_proto(proto) -> "VolumeDef":
        return VolumeDef(json_payload=proto.json)

    @staticmethod
    def _get_range_step(method) -> int:
        """Given a range method, find the step size"""
        range_ = method["range"]
        if len(range_) == 3:
            return range_[2]
        else:
            # Accounting for negative ranges
            if range_[0] < range_[1]:
                return 1
            else:
                return -1

    @staticmethod
    def _iterate_method(method) -> Iterable[int]:
        """Given a volumedef method, iterate over each minor number in it."""
        if "list" in method:
            return method["list"]
        elif "range" in method:
            lower, upper = method["range"][0:2]
            step = VolumeDef._get_range_step(method)
            range_ = [x for x in range(lower, upper + step, step)]
            if range_[-1] > upper:
                # Needed because range() will go up to one element beyond upper+step if it isn't cleanly divisible.
                range_.pop()
            return range_

    @staticmethod
    def _iterate_methods(methods) -> Iterable[int]:
        "Given a list of volumedef methods, iterate over each number described by it"
        for method in methods:
            for value in VolumeDef._iterate_method(method):
                yield value

    @staticmethod
    def _get_method_size(method, minor_range: Optional[Tuple[int, int]] = None) -> int:
        """Given a volumedef method, calculate the number of traces within it and minor_range"""
        c = 0
        if "list" in method:
            if minor_range is None:
                c += len(method["list"])
            else:
                for minor in method["list"]:
                    if minor < minor_range[0] or minor > minor_range[1]:
                        continue
                    c += 1
        elif "range" in method:
            start, stop = method["range"][0:2]
            step = VolumeDef._get_range_step(method)
            # Let's simplify to a positive range, shall we?
            if start > stop:
                start, stop = stop, start
                step = -step
            if minor_range is not None:
                if start < minor_range[0]:
                    # This computes the ceiling of (minor_range[0] - start) / step
                    nsteps = (minor_range[0] - start + step - 1) // step
                    start = start + step * nsteps
                if stop > minor_range[1]:
                    stop = minor_range[1]
            if stop >= start:
                c += (stop - start) // step + 1
        else:
            raise Exception(f"The specified method {method} was not recognized.")

        return c

    @staticmethod
    def _get_method_range(method) -> Tuple[int, int]:
        """Given a method, find the minimum and maximum coordinates within it"""
        if "list" in method:
            minimum = min(method["list"])
            maximum = max(method["list"])
            return (minimum, maximum)
        elif "range" in method:
            lower, upper = method["range"][0:2]
            step = VolumeDef._get_range_step(method)

            # Find highest multiple of step not greater than upper
            end = lower + ((upper - lower) // step) * step

            return tuple(sorted((lower, end)))  # Sort to handle negative-step volumedefs
        else:
            raise Exception(f"The specified method {method} was not recognized.")

    def count_line_traces(
        self, inline_range: Optional[Tuple[int, int]] = None, xline_range: Optional[Tuple[int, int]] = None
    ) -> Mapping[int, int]:
        """Count the number of traces by line, optionally restricted by ranges.

        Returns:
            Mapping[int, int]: A mapping of line number to trace count.
        """
        if self.parsed["version"] >= 200:
            raise Exception(
                f'The specified volumedef version {self.parsed["version"]} is not supported by this version of the Cognite SDK.'
            )
        output = {}
        if self.direction == Direction.INLINE:
            major_range, minor_range = inline_range, xline_range
        else:
            major_range, minor_range = xline_range, inline_range
        for key, methods in self.parsed["lines"].items():
            key = int(key)
            if major_range and (key < major_range[0] or key > major_range[1]):
                continue
            c = 0
            for method in methods:
                c += VolumeDef._get_method_size(method, minor_range)
            output[key] = c
        return output

    def count_total_traces(
        self, inline_range: Optional[Tuple[int, int]] = None, xline_range: Optional[Tuple[int, int]] = None
    ) -> int:
        """Count the total number of traces in this volumedef, optionally restricted by ranges."""
        c = 0
        traces = self.count_line_traces(inline_range, xline_range)
        for val in traces.values():
            c += val
        return c

    def get_major_range(self) -> Mapping[int, Tuple[int, int]]:
        """Return the min & max range of traces by major line, i.e. a mapping from major number to minor range.

        Returns:
            Mapping[int, Tuple[int, int]]: A mapping of line number to minimum and maximum value for that line.
        """
        output = {}
        for key, methods in self.parsed["lines"].items():
            lower, upper = None, None
            for x, y in map(VolumeDef._get_method_range, methods):
                if lower is None or x < lower:
                    lower = x
                if upper is None or upper < y:
                    upper = y
            output[int(key)] = (lower, upper)
        return output

    def get_minor_range(self) -> Mapping[int, Tuple[int, int]]:
        """Return the min & max range of traces by minor line, i.e. a mapping from minor number to major range.

        Returns:
            Mapping[int, Tuple[int, int]]: A mapping of line number to minimum and maximum value for that line.
        """
        output = {}
        for key, methods in self.parsed["lines"].items():
            for minor in VolumeDef._iterate_methods(methods):
                lower, upper = output.setdefault(minor, (None, None))
                if lower is None or int(key) < lower:
                    lower = int(key)
                if upper is None or int(key) > upper:
                    upper = int(key)
                output[minor] = (lower, upper)
        return output

    def get_inline_range(self) -> Mapping[int, Tuple[int, int]]:
        """Return the min & max range of traces by inline. That is, the mapping will be from inline numbers to xline numbers.

        Returns:
            Mapping[int, Tuple[int, int]]: A mapping of line number to minimum and maximum value for that line.
        """
        if self.direction == Direction.INLINE:
            return self.get_major_range()
        else:
            return self.get_minor_range()

    def get_xline_range(self) -> Mapping[int, Tuple[int, int]]:
        """Return the min & max range of traces by xline. That is, the mapping will be from xline numbers to inline numbers.

        Returns:
            Mapping[int, Tuple[int, int]]: A mapping of line number to minimum and maximum value for that line.
        """
        if self.direction == Direction.XLINE:
            return self.get_major_range()
        else:
            return self.get_minor_range()

    def common_major_range(self) -> RangeInclusive:
        """Compute the range with the largest step size encompassing all major lines in this VolumeDef

        Returns:
            RangeInclusive: Range describing the minimum, maximum, and step size of line numbers
        """
        majors = [int(major) for major in self.parsed["lines"].keys()]
        min_major = min(majors)
        max_major = max(majors)
        step = max_major - min_major
        if step == 0:
            # A single major line only. Set step = 1 for simplicity.
            return RangeInclusive(min_major, max_major, 1)
        for major in majors:
            if major < min_major or major > max_major:
                continue
            step = math.gcd(step, major - min_major)
            if step == 1:
                break
        return RangeInclusive(min_major, max_major, step)

    def common_minor_range(self) -> RangeInclusive:
        """Compute the range with the largest step size encompassing all minor lines in this VolumeDef

        Returns:
            RangeInclusive: Range describing the minimum, maximum, and step size of line numbers
        """
        ranges = self.get_major_range().values()
        min_minor = min(r[0] for r in ranges)
        max_minor = max(r[1] for r in ranges)
        step = max_minor - min_minor
        if step == 0:
            # A single minor value. Set step = 1 for simplicity.
            return RangeInclusive(min_minor, max_minor, 1)
        for methods in self.parsed["lines"].values():
            # Let's be stupid for now and just check all lines
            # This can be optimized by not iterating through the ranges
            for minor in self._iterate_methods(methods):
                step = math.gcd(step, minor - min_minor)
                if step == 1:
                    return RangeInclusive(min_minor, max_minor, step)
        return RangeInclusive(min_minor, max_minor, step)

    def common_inline_range(self) -> RangeInclusive:
        """Compute the range with the largest step size encompassing all inlines in this VolumeDef

        Returns:
            RangeInclusive: Range describing the minimum, maximum, and step size of line numbers
        """
        if self.direction == Direction.INLINE:
            return self.common_major_range()
        else:
            return self.common_minor_range()

    def common_xline_range(self) -> RangeInclusive:
        """Compute the range with the largest step size encompassing all xlines in this VolumeDef

        Returns:
            RangeInclusive: Range describing the minimum, maximum, and step size of line numbers
        """
        if self.direction == Direction.XLINE:
            return self.common_major_range()
        else:
            return self.common_minor_range()

    def max_ranges(self) -> Tuple[RangeInclusive, RangeInclusive]:
        ranges = self.get_major_range()
        major = RangeInclusive(min(ranges.keys()), max(ranges.keys()))
        minor = RangeInclusive.widest(ranges.values())
        if self.direction == Direction.INLINE:
            return (major, minor)
        else:
            return (minor, major)


class File:
    """Represents a raw SEGY file.

    Attributes:
        id (str): The id of the file
        name (str): The name of the file
        metadata (Mapping[str, str]): Any custom-defined metadata for the file
        is_temporary (bool): `True` if the file is temporary.
    """

    id: str
    name: str
    metadata: Mapping[str, str]
    is_temporary: bool

    def __init__(self, *, id, name, metadata, is_temporary):
        self.id = id
        self.name = name
        self.metadata = metadata
        self.is_temporary = is_temporary

    def __repr__(self):
        temporary = ", temporary" if self.is_temporary else ""
        return f"File<id: {self.id}, name: {self.name}{temporary}, metadata: {metadata}>"

    @staticmethod
    def from_proto(proto) -> "File":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]
        return File(id=proto.id, name=proto.name, metadata=metadata, is_temporary=proto.is_temporary)


class Geometry:
    """Represents a CRS + shape, in either a WKT format or a GeoJSON.

    Attributes:
        crs (str): The CRS of the shape.
        geojson (Optional[dict]): If exists, the GeoJSON representation of this shape
        wkt (Optional[str]): If exists, the Well Known Text representation of this shape
    """

    crs: str
    geojson: Optional[dict]
    wkt: Optional[str]

    def __init__(self, crs: str, *, geojson=None, wkt=None):
        if (geojson is None) and (wkt is None):
            raise ValueError("You must specify one of: geojson, wkt")
        if (geojson is not None) and (wkt is not None):
            raise ValueError("You must specify either of: geojson, wkt")
        self.crs = crs
        self.geojson = geojson
        self.wkt = wkt

    def __repr__(self):
        if self.geojson:
            return f"Geometry<crs: {self.crs}, geojson: {self.geojson}>"
        else:
            return f"Geometry<crs: {self.crs}, wkt: {self.wkt}>"

    @staticmethod
    def from_proto(proto) -> Union["Geometry", None]:
        """Convert a Geometry proto into a Geometry object.

        May return None if neither geojson nor wkt are specified.
        """
        crs = proto.crs.crs
        geojson = MessageToDict(proto.geo.json) or None
        wkt = proto.wkt.geometry or None
        if geojson is None and wkt is None:
            return None
        return Geometry(crs=crs, geojson=geojson, wkt=wkt)

    def to_proto(self):
        crs_proto = CRSProto(crs=self.crs)
        if self.geojson is not None:
            return GeometryProto(crs=crs_proto, geo=GeoJson(json=self.geojson))
        if self.wkt is not None:
            return GeometryProto(crs=crs_proto, wkt=Wkt(geometry=self.wkt))


class TextHeader:
    """A representation of text headers used to create or edit existing headers.

    Attributes:
        header (Optional[str]): The text content of the header
        raw_header (Optional[str]): The raw bytes of a header as a string
    """

    def __init__(self, *, header: MaybeString = None, raw_header: MaybeString = None):
        """Create a text header.

        Specify either header or raw_header.

        Args:
            header (str | None): The text content of a header
            raw_header (str | None): The raw bytes of a header
        """
        self.header = header
        self.raw_header = raw_header

    def __repr__(self):
        return f"TextHeader<{self.header}>"

    def from_proto(proto):
        return TextHeader(header=proto.header, raw_header=proto.raw_header)

    def into_proto(self):
        return TextHeaderProto(header=self.header, raw_header=self.raw_header)


class BinaryHeader:
    """A representation of binary headers used to create or edit existing headers.

    BinaryHeader.FIELDS contains the list of valid fields. to set after the object is constructed.

    Attributes:
        traces
        trace_data_type
        fixed_length_traces
        segy_revision
        auxtraces
        interval
        interval_original
        samples
        samples_original
        ensemble_fold
        vertical_sum
        trace_type_sorting_code
        sweep_type_code
        sweep_frequency_start
        sweep_frequency_end
        sweep_length
        sweep_channel
        sweep_taper_start
        sweep_taper_end
        sweep_taper_type
        correlated_traces
        amplitude_recovery
        original_measurement_system
        impulse_signal_polarity
        vibratory_polarity_code
    """

    FIELDS = (
        "traces",
        "trace_data_type",
        "fixed_length_traces",
        "segy_revision",
        "auxtraces",
        "interval",
        "interval_original",
        "samples",
        "samples_original",
        "ensemble_fold",
        "vertical_sum",
        "trace_type_sorting_code",
        "sweep_type_code",
        "sweep_frequency_start",
        "sweep_frequency_end",
        "sweep_length",
        "sweep_channel",
        "sweep_taper_start",
        "sweep_taper_end",
        "sweep_taper_type",
        "correlated_traces",
        "amplitude_recovery",
        "original_measurement_system",
        "impulse_signal_polarity",
        "vibratory_polarity_code",
    )

    def __init__(self, *args, raw_header: Union[bytes, None] = None, **kwargs):
        """Initialize.

        Args:
            *args (int): An optional list of arguments. The fields are assigned to the binary_header fields in sequential order, and missing fields are assigned None.
            **kwargs (int): An optional key-value mapping of arguments, which overwrite any values from *args.
            raw_header (bytes | None): Optional raw header.
        """
        for i, field in enumerate(BinaryHeader.FIELDS):
            val = args[i] if i < len(args) else None
            val = kwargs[field] if field in kwargs else val
            setattr(self, field, val)
        self.raw_header = raw_header

    def __repr__(self):
        fields = []
        for field in self.FIELDS:
            val = getattr(self, field)
            if val is not None:
                fields.append(f"{field}: {val}")
        fields = ", ".join(fields)
        return f"BinaryHeader<{fields}>"

    @staticmethod
    def from_proto(proto) -> "BinaryHeader":
        return BinaryHeader(
            traces=proto.traces,
            trace_data_type=proto.trace_data_type,
            fixed_length_traces=proto.fixed_length_traces,
            segy_revision=proto.segy_revision,
            auxtraces=proto.auxtraces,
            interval=proto.interval,
            interval_original=proto.interval_original,
            samples=proto.samples,
            samples_original=proto.samples_original,
            ensemble_fold=proto.ensemble_fold,
            vertical_sum=proto.vertical_sum,
            trace_type_sorting_code=proto.trace_type_sorting_code,
            sweep_type_code=proto.sweep_type_code,
            sweep_frequency_start=proto.sweep_frequency_start,
            sweep_frequency_end=proto.sweep_frequency_end,
            sweep_length=proto.sweep_length,
            sweep_channel=proto.sweep_channel,
            sweep_taper_start=proto.sweep_taper_start,
            sweep_taper_end=proto.sweep_taper_end,
            sweep_taper_type=proto.sweep_taper_type,
            correlated_traces=proto.correlated_traces,
            amplitude_recovery=proto.amplitude_recovery,
            original_measurement_system=proto.original_measurement_system,
            impulse_signal_polarity=proto.impulse_signal_polarity,
            vibratory_polarity_code=proto.vibratory_polarity_code,
            raw_header=proto.raw_header,
        )

    def into_proto(self):
        return BinaryHeaderProto(
            traces=self.traces,
            trace_data_type=self.trace_data_type,
            fixed_length_traces=self.fixed_length_traces,
            segy_revision=self.segy_revision,
            auxtraces=self.auxtraces,
            interval=self.interval,
            interval_original=self.interval_original,
            samples=self.samples,
            samples_original=self.samples_original,
            ensemble_fold=self.ensemble_fold,
            vertical_sum=self.vertical_sum,
            trace_type_sorting_code=self.trace_type_sorting_code,
            sweep_type_code=self.sweep_type_code,
            sweep_frequency_start=self.sweep_frequency_start,
            sweep_frequency_end=self.sweep_frequency_end,
            sweep_length=self.sweep_length,
            sweep_channel=self.sweep_channel,
            sweep_taper_start=self.sweep_taper_start,
            sweep_taper_end=self.sweep_taper_end,
            sweep_taper_type=self.sweep_taper_type,
            correlated_traces=self.correlated_traces,
            amplitude_recovery=self.amplitude_recovery,
            original_measurement_system=self.original_measurement_system,
            impulse_signal_polarity=self.impulse_signal_polarity,
            vibratory_polarity_code=self.vibratory_polarity_code,
            raw_header=self.raw_header,
        )


class SeismicStore:
    """Represents a seismic store.

    Attributes:
        id (int): The unique internal id of the seismic store.
        name (str): The unique name of the seismic store. Will be changed to external-id in the future.
        survey_id (str): The survey this seismic store belongs to.
        ingestion_source (:py:class:`IngestionSource`): The source of the seismicstore.
        metadata (Mapping[str, str]): Any custom-defined metadata
        ingested_file (Optional[:py:class:`File`]): If present, the file this SeismicStore was ingested from
        inline_volume_def (Optional[:py:class:`VolumeDef`]): The inline-major volume definition for this seismic store.
        xline_volume_def (Optional[:py:class:`VolumeDef`]): The xline-major volume definition for this seismic store.
        coverage (Optional[:py:class:`Geometry`]): If present, the coverage geometry for this seismic store
        text_header (Optional[:py:class:`TextHeader`]): If present, the text header for this seismic store
        binary_header (Optional[:py:class:`BinaryHeader`]): If present, the binary header for this seismic store
        storage_tier_name (List[str]): The names of the storage tiers this seismic store exists in
    """

    id: int
    name: str
    survey_id: str
    ingestion_source: IngestionSource
    metadata: Mapping[str, str]
    ingested_file: Optional[File]
    inline_volume_def: Optional[VolumeDef]
    xline_volume_def: Optional[VolumeDef]
    coverage: Geometry
    text_header: Optional[TextHeader]
    binary_header: Optional[BinaryHeader]
    storage_tier_name: List[str]

    def __init__(
        self,
        *,
        id,
        name,
        survey_id,
        ingestion_source,
        metadata,
        ingested_file,
        inline_volume_def,
        xline_volume_def,
        coverage,
        text_header,
        binary_header,
        storage_tier_name,
    ):
        self.id = id
        self.name = name
        self.survey_id = survey_id
        self.ingestion_source = ingestion_source
        self.metadata = metadata
        self.ingested_file = ingested_file
        self.inline_volume_def = inline_volume_def
        self.xline_volume_def = xline_volume_def
        self.coverage = coverage
        self.text_header = text_header
        self.binary_header = binary_header
        self.storage_tier_name = storage_tier_name

    def __repr__(self):
        return f"SeismicStore<id: {self.id}, name: {self.name}, survey_id: {self.survey_id}, ingestion_source: {self.ingestion_source}, metadata: {self.metadata}, storage_tier: {self.storage_tier_name}>"

    @staticmethod
    def from_proto(proto) -> "SeismicStore":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]

        # Only decode protobuf fields that are defined.
        inline_volume_def = None
        xline_volume_def = None
        coverage = None
        text_header = None
        binary_header = None
        if proto.HasField("inline_volume_def"):
            inline_volume_def = VolumeDef.from_proto(proto.inline_volume_def)
        if proto.HasField("crossline_volume_def"):
            xline_volume_def = VolumeDef.from_proto(proto.crossline_volume_def)
        if proto.HasField("coverage"):
            coverage = Geometry.from_proto(proto.coverage)
        if proto.HasField("text_header"):
            text_header = TextHeader.from_proto(proto.text_header)
        if proto.HasField("binary_header"):
            binary_header = BinaryHeader.from_proto(proto.binary_header)

        return SeismicStore(
            id=proto.id,
            name=proto.name,
            survey_id=proto.survey_id,
            ingestion_source=proto.ingestion_source,
            metadata=metadata,
            ingested_file=proto.ingested_file,
            inline_volume_def=inline_volume_def,
            xline_volume_def=xline_volume_def,
            coverage=coverage,
            text_header=text_header,
            binary_header=binary_header,
            storage_tier_name=proto.storage_tier_name,
        )


class SeismicLineRange:
    """Represents the line range for a seismic"""

    inline_min: int
    inline_max: int
    inline_step: int
    xline_min: int
    xline_max: int
    xline_step: int

    def __init__(self, inline_min, inline_max, inline_step, xline_min, xline_max, xline_step):
        self.inline_min = inline_min
        self.inline_max = inline_max
        self.inline_step = inline_step
        self.xline_min = xline_min
        self.xline_max = xline_max
        self.xline_step = xline_step

    def __repr__(self):
        return (
            "SeismicLineRange<"
            f"inline_min: {self.inline_min}, "
            f"inline_max: {self.inline_max}, "
            f"inline_step: {self.inline_step}, "
            f"xline_min: {self.xline_min}, "
            f"xline_max: {self.xline_max}, "
            f"xline_step: {self.xline_step}>"
        )

    @staticmethod
    def from_proto(proto) -> "SeismicLineRange":
        return SeismicLineRange(
            inline_min=proto.inline.min.value,
            inline_max=proto.inline.max.value,
            inline_step=proto.inline.step.value,
            xline_min=proto.crossline.min.value,
            xline_max=proto.crossline.max.value,
            xline_step=proto.crossline.step.value,
        )


class Seismic:
    """Represents a seismic, a cutout of a seismic store.

    Attributes:
        id (int): The unique internal id of the seismic
        external_id (str): The external id of the seismic
        crs (str): The Coordinate Reference System of the seismic
        metadata (Mapping[str, str]): Any custom-defined metadata
        text_header (Optional[:py:class:`TextHeader`]): The text header that corresponds to the seismic
        binary_header (Optional[:py:class:`BinaryHeader`]): The binary header that corresponds to the seismic
        line_range: TODO
        volume_def (Optional[:py:class:`VolumeDef`]): The VolumeDef describing the seismic
        partition_id (int): The id of the partition the seismic belongs to
        seismicstore_id (int): The id of the seismicstore the seismic is derived from
        coverage (Optional[:py:class:`Geometry`]): The coverage geometry for the seismic.
    """

    id: int
    external_id: str
    name: str
    crs: str
    metadata: Mapping[str, str]
    text_header: Optional[TextHeader]
    binary_header: Optional[BinaryHeader]
    line_range: Optional[SeismicLineRange]
    volume_def: Optional[VolumeDef]
    partition_id: int
    seismicstore_id: Optional[int]
    coverage: Optional[Geometry]

    def __init__(
        self,
        *,
        id,
        external_id,
        name,
        crs,
        metadata,
        text_header,
        binary_header,
        line_range,
        volume_def,
        partition_id,
        seismicstore_id,
        coverage,
    ):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.crs = crs
        self.metadata = metadata
        self.text_header = text_header
        self.binary_header = binary_header
        self.line_range = line_range
        self.volume_def = volume_def
        self.partition_id = partition_id
        self.seismicstore_id = seismicstore_id
        self.coverage = coverage

    def __repr__(self):
        return f"Seismic<id: {self.id}, external_id: {self.external_id}, name: {self.name}, crs: {self.crs}, metadata: {self.metadata}>"

    @staticmethod
    def from_proto(proto) -> "Seismic":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]

        # Only decode protobuf fields that are defined.
        text_header = None
        binary_header = None
        line_range = None
        volume_def = None
        coverage = None
        if proto.HasField("text_header"):
            text_header = TextHeader.from_proto(proto.text_header)
        if proto.HasField("binary_header"):
            binary_header = BinaryHeader.from_proto(proto.binary_header)
        if proto.HasField("line_range"):
            line_range = SeismicLineRange.from_proto(proto.line_range)
        if proto.HasField("volume_def"):
            volume_def = VolumeDef.from_proto(proto.volume_def)
        if proto.HasField("coverage"):
            coverage = Geometry.from_proto(proto.coverage)

        return Seismic(
            id=proto.id,
            external_id=proto.external_id,
            name=proto.name,
            crs=proto.crs,
            metadata=metadata,
            text_header=text_header,
            binary_header=binary_header,
            line_range=line_range,
            volume_def=volume_def,
            partition_id=proto.partition_id,
            seismicstore_id=proto.seismicstore_id,
            coverage=coverage,
        )


class Partition:
    """Represents a partition and its included seismics

    Attributes:
        id (int): The unique internal id for this partition
        name (str): The human-friendly name for this partition
        seismics (List[:py:class:`Seismic`]): The list of seismics that belong to this partition
    """

    id: int
    external_id: str
    name: str
    seismics: List[Seismic]

    def __init__(self, *, id, external_id, name, seismics):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.seismics = seismics

    def __repr__(self):
        return f"Partition<id: {self.id}, external_id: {self.external_id}, name: {self.name}>"

    @staticmethod
    def from_proto(proto) -> "Partition":
        seismics = [Seismic.from_proto(s) for s in proto.seismics]
        return Partition(id=proto.id, external_id=proto.external_id, name=proto.name, seismics=seismics)


class Survey:

    id: str
    external_id: Optional[str]
    name: str
    seismic_ids: Optional[List[int]]
    seismic_store_ids: Optional[List[int]]
    metadata: Optional[Mapping[str, str]]
    coverage: Optional[Geometry]

    def __init__(self, id, external_id, name, seismic_ids, seismic_store_ids, metadata, coverage):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.seismic_ids = seismic_ids
        self.seismic_store_ids = seismic_store_ids
        self.metadata = metadata
        self.coverage = coverage

    @staticmethod
    def from_proto(proto) -> "Survey":
        survey_id = proto.survey.id
        external_id = None
        name = proto.survey.name if hasattr(proto.survey, "name") else None
        metadata = proto.survey.metadata if hasattr(proto.survey, "metadata") else None
        seismic_ids = proto.seismic_ids if hasattr(proto, "seismic_ids") else None
        seismic_store_ids = proto.seismic_store_ids if hasattr(proto, "seismic_store_ids") else None
        coverage = Geometry.from_proto(proto.coverage) if proto.HasField("coverage") else None

        return Survey(survey_id, external_id, name, seismic_ids, seismic_store_ids, metadata, coverage)

    def __repr__(self):
        return "%s {\n%s\n}" % (type(self).__name__, "\n".join("%s = %s" % item for item in vars(self).items()))

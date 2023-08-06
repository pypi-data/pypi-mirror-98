import os
import sys
from typing import *

import numpy as np
import numpy.ma as ma
from cognite.seismic._api.api import API
from cognite.seismic._api.file import FileAPI

if not os.getenv("READ_THE_DOCS"):

    from cognite.seismic.protos.query_service_messages_pb2 import LineSlabRequest, Horizon
    from cognite.seismic.protos.types_pb2 import LineBasedRectangle, PositionQuery
    from google.protobuf.wrappers_pb2 import Int32Value


class SlabAPI(API):
    def __init__(self, query, file_api: FileAPI, metadata):
        super().__init__(query=query, metadata=metadata)
        self.file_api = file_api

    def get(
        self,
        file_id: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_range: Tuple[int, int] = None,
        xline_range: Tuple[int, int] = None,
        z: int = None,
        horizon: List[List[int]] = None,
        n_below: int = None,
        n_above: int = None,
    ):

        """Get a seismic slab along a horizon or constant depth bounded by inline and xline ranges

        Args:
            file_id (str, optional): File can be specified either by name or id (id will be used first if both are provided)
            file_name (str, optional): File can be specified either by name or id (id will be used first if both are provided)
            inline_range (int tuple, optional): filter volume by min and max inline indices
            xline_range (int tuple, optional): filter volume by min and max xline indices
            n_below (int, optional): number of trace values to retrieve above given horizon/depth
            n_above (int, optional): number of trace values to retrieve below given horizon/depth
            z (int): The depth index to return
            horizon (List[List[int]], optional): The horizon to use as the depth indices across the returned traces

        Returns:
            Volume of trace data represented an masked numpy array with dimensions (inline, xline, trace)
        """

        file = self.identify(file_id, file_name)

        if inline_range is None or xline_range is None:
            range = (
                self.file_api.get_line_range(file_id=file_id)
                if file_id is not None
                else self.file_api.get_line_range(file_name=file_name)
            )
            if inline_range is None:
                inline_range = (range.inline.min, range.inline.max)
            if xline_range is None:
                xline_range = (range.xline.min, range.xline.max)

        top_left = PositionQuery(iline=inline_range[0], xline=xline_range[0])
        bottom_right = PositionQuery(iline=inline_range[1], xline=xline_range[1])
        rectangle = LineBasedRectangle(top_left=top_left, bottom_right=bottom_right)

        if z is None and horizon is None:
            raise ValueError("either z or horizon must be specified")

        if n_below is None:
            n_below = 0
        else:
            if n_below < 0:
                raise ValueError("n_below must be positive")
        if n_above is None:
            n_above = 0
        else:
            if n_above < 0:
                raise ValueError("n_above must be positive")

        zmin = sys.maxsize
        zmax = 0
        if z is not None:
            zmin = max(0, z - n_below)
            zmax = z + n_above
            request = LineSlabRequest(file=file, rectangle=rectangle, constant=z, n_below=n_below, n_above=n_above)
        else:
            flat_horizon = [index for inline_horizon in horizon for index in inline_horizon]
            for z in flat_horizon:
                temp_min_z = max(0, z - n_below)
                temp_max_z = z + n_above
                if temp_min_z < zmin:
                    zmin = temp_min_z
                if temp_max_z > zmax:
                    zmax = temp_max_z
            request = LineSlabRequest(
                file=file,
                rectangle=rectangle,
                horizon=Horizon(z_values=flat_horizon),
                n_below=Int32Value(value=n_below),
                n_above=Int32Value(value=n_above),
            )

        inline_dim = inline_range[1] - inline_range[0] + 1
        xline_dim = xline_range[1] - xline_range[0] + 1
        z_dim = zmax - zmin + 1

        dims = (inline_dim, xline_dim, z_dim)

        output_unmasked = np.full(dims, np.nan, dtype=np.float32)
        mask = np.full(dims, True, dtype=np.bool)

        output = ma.array(data=output_unmasked, dtype=np.float32, copy=False, mask=mask)

        stream = self.query.GetSlabByLines(request, metadata=self.metadata)
        for s in stream:
            inline_index = s.trace.iline.value - inline_range[0]
            xline_index = s.trace.xline.value - xline_range[0]
            output[inline_index][xline_index][(s.z_from - zmin) : (s.z_to + 1 - zmin)] = s.trace.trace

        return output

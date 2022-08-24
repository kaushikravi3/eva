# coding=utf-8
# Copyright 2018-2022 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np
import pandas as pd

from eva.udfs.ndarray_udfs.abstract_ndarray_udfs import AbstractNdarrayUDF
from eva.utils.logging_manager import logger


class Crop(AbstractNdarrayUDF):
    def name(self):
        return "Crop"

    def exec(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Crop the frame given the bbox.
        Crop(frame, bbox)
        If one of the side of the crop box is 0, it automatically sets it to 1 pixel

        """

        def crop(row: pd.Series) -> np.ndarray:
            frame = row[0]
            bboxes = row[1]
            try:
                x0, y0, x1, y1 = np.asarray(bboxes, dtype="int")
                x0 = max(0, x0)
                y0 = max(0, y0)
                if x1 == x0 :
                    x1 = x0 + 1
                if y1 == y0 :
                    y1 = y0 + 1
                output = frame[y0:y1, x0:x1]
                ss = output.shape
                assert ss[0] > 0
                assert ss[1] > 0
            except Exception as e:
                logger.warn(f"Invalid input to crop {e}")
            return frame

        ret = pd.DataFrame()
        ret["cropped_frame_array"] = df.apply(crop, axis=1)

        return ret
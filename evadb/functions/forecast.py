# coding=utf-8
# Copyright 2018-2023 EvaDB
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


import pickle

import pandas as pd

from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import setup


class ForecastModel(AbstractFunction):
    @property
    def name(self) -> str:
        return "ForecastModel"

    @setup(cacheable=False, function_type="Forecasting", batchable=True)
    def setup(
        self,
        model_name: str,
        model_path: str,
        predict_column_rename: str,
        time_column_rename: str,
        id_column_rename: str,
        horizon: int,
        library: str,
    ):
        self.library = library
        if "neuralforecast" in self.library:
            from neuralforecast import NeuralForecast

            loaded_model = NeuralForecast.load(path=model_path)
            self.model_name = model_name[4:] if "Auto" in model_name else model_name
        else:
            with open(model_path, "rb") as f:
                loaded_model = pickle.load(f)
            self.model_name = model_name
        self.model = loaded_model
        self.predict_column_rename = predict_column_rename
        self.time_column_rename = time_column_rename
        self.id_column_rename = id_column_rename
        self.horizon = int(horizon)

    def forward(self, data) -> pd.DataFrame:
        if self.library == "statsforecast":
            forecast_df = self.model.predict(h=self.horizon)
        else:
            forecast_df = self.model.predict()
        forecast_df.reset_index(inplace=True)
        forecast_df = forecast_df.rename(
            columns={
                "unique_id": self.id_column_rename,
                "ds": self.time_column_rename,
                self.model_name: self.predict_column_rename,
            }
        )[: self.horizon * forecast_df["unique_id"].nunique()]
        return forecast_df

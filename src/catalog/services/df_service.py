# coding=utf-8
# Copyright 2018-2020 EVA
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
from typing import List

from sqlalchemy.orm.exc import NoResultFound

from src.catalog.models.df_metadata import DataFrameMetadata
from src.catalog.services.base_service import BaseService
from src.utils.logging_manager import LoggingManager, LoggingLevel


class DatasetService(BaseService):
    def __init__(self):
        super().__init__(DataFrameMetadata)

    def create_dataset(self, name, file_url) -> DataFrameMetadata:
        """
        Create a new dataset entry for given name and file URL.
        Arguments:
            name (str): name of the dataset
            file_url (str): file path of the dataset.

        Returns:
            DataFrameMetadata object
        """
        metadata = self.model(name=name, file_url=file_url)
        metadata = metadata.save()
        return metadata

    def dataset_by_name(self, name: str) -> int:
        """
        Returns metadata id for the name queried

        Arguments:
            name (str)- Name for which id is required

        Returns:
            int (dataset id)
        """
        try:
            result = self.model.query \
                .with_entities(self.model._id) \
                .filter(self.model._name == name).one()
            return result[0]
        except NoResultFound:
            LoggingManager().log(
                "get_id_from_name failed with name {}".format(name),
                LoggingLevel.ERROR)

    def dataset_by_id(self, dataset_id) -> DataFrameMetadata:
        """
        Returns the dataset by ID
        Arguments:
            dataset_id (int)
        Returns:
           DataFrameMetadata
        """
        return self.model.query \
            .filter(self.model._id == dataset_id) \
            .one()

    def dataset_object_by_name(self, database_name, dataset_name,
                               column_name: List[str] = None):
        """
        Get the metadata for the given table.
        Arguments:
            database_name  (str): Database to which dataset belongs # TODO:
            use this field
            dataset_name (str): name of the dataset
            column_name (List[str]): list of columns for the  dataset which
            need be listed. If not specified, all columns will be retrieved
            # TODO:  perform column filtering when column_name not None
        Returns:
            DataFrameMetadata - metadata for given dataset_name
        """
        return self.model.query.filter(
            self.model._name == dataset_name).one()
        
    def delete_dataset(self, metadata_id):
        try:
            result = self.model.query \
            .filter(self.model._id == metadata_id) \
            .one()

            result.delete()

        except Exception:
            LoggingManager().log(
                "detele datset failed with id {}".format(metadata_id),
                LoggingLevel.ERROR)
            raise Exception



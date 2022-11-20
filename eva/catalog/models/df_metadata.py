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
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from eva.catalog.df_schema import DataFrameSchema
from eva.catalog.models.base_model import BaseModel


class DataFrameMetadata(BaseModel):
    __tablename__ = "df_metadata"

    _name = Column("name", String(100), unique=True)
    _file_url = Column("file_url", String(100))
    _unique_identifier_column = Column("identifier_column", String(100))
    _is_video = Column("is_video", Boolean)
    _columns = relationship(
        "DataFrameColumn",
        back_populates="_dataset",
        cascade="all, delete, delete-orphan",
    )

    def non_copy_constructor(
        self, name: str, file_url: str, identifier_id="id", is_video=False
    ):
        self._name = name
        self._file_url = file_url
        self._schema = None
        self._unique_identifier_column = identifier_id
        self._is_video = is_video

    # copy constructor used to typecast DataFrameMetadata to TableMetadata
    def copy_constructor(self, object):
        self._name = object.name
        self._file_url = object.file_url
        self._schema = object.Schema
        self._unique_identifier_column = object.identifier_id
        self._is_video = object.is_video

    def __init__(self, *args):
        if len(args) > 1:
            self.non_copy_constructor(*args)
        else:
            self.copy_constructor(args)

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, column_list):
        self._schema = DataFrameSchema(self._name, column_list)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def file_url(self):
        return self._file_url

    @property
    def columns(self):
        return self._columns

    @property
    def identifier_column(self):
        return self._unique_identifier_column

    @property
    def is_video(self):
        return self._is_video

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.file_url == other.file_url
            and self.schema == other.schema
            and self.identifier_column == other.identifier_column
            and self.name == other.name
            and self.is_video == other.is_video
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.id,
                self.file_url,
                self.schema,
                self.identifier_column,
                self.name,
                self.is_video,
            )
        )


# Create a table metadata class which has the same attributes, properties and methods as DataFrameMetadata,
# but without any links to its base class (SQLLite session object isn't a member of it)
TableMetadata = type("TableMetadata", (), vars(DataFrameMetadata))

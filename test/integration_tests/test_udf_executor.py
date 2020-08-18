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
import unittest
import os
import pandas as pd

from src.catalog.catalog_manager import CatalogManager
from src.models.storage.batch import Batch
from test.util import create_sample_video, perform_query
from test.util import DummyObjectDetector

NUM_FRAMES = 10


class UDFExecutorTest(unittest.TestCase):

    def setUp(self):
        CatalogManager().reset()
        create_sample_video()

    def tearDown(self):
        os.remove('dummy.avi')

    # integration test
    def test_should_load_and_select_using_udf_video_in_table(self):
        load_query = """LOAD DATA INFILE 'dummy.avi' INTO MyVideo;"""
        perform_query(load_query)

        create_udf_query = """CREATE UDF DummyObjectDetector
                  INPUT  (Frame_Array NDARRAY (3, 256, 256))
                  OUTPUT (label TEXT(10))
                  TYPE  Classification
                  IMPL  'test/util.py';
        """
        perform_query(create_udf_query)

        select_query = "SELECT id,DummyObjectDetector(data) FROM MyVideo;"
        actual_batch = perform_query(select_query)
        labels = DummyObjectDetector().labels
        expected = [{'id': i, 'label': labels[1 + i % 2]}
                    for i in range(NUM_FRAMES)]
        expected_batch = Batch(frames=pd.DataFrame(expected))
        self.assertEqual(actual_batch, expected_batch)

    def test_should_load_and_select_using_udf_video(self):
        load_query = """LOAD DATA INFILE 'dummy.avi' INTO MyVideo;"""
        perform_query(load_query)

        create_udf_query = """CREATE UDF DummyObjectDetector
                  INPUT  (Frame_Array NDARRAY (3, 256, 256))
                  OUTPUT (label TEXT(10))
                  TYPE  Classification
                  IMPL  'test/util.py';
        """
        perform_query(create_udf_query)

        select_query = "SELECT id,DummyObjectDetector(data) FROM MyVideo \
            WHERE DummyObjectDetector(data).label = 'person';"
        actual_batch = perform_query(select_query)
        labels = DummyObjectDetector().labels
        expected = [{'id': i * 2, 'label': labels[1 + i % 2]}
                    for i in range(NUM_FRAMES // 2)]
        expected_batch = Batch(frames=pd.DataFrame(expected))
        self.assertEqual(actual_batch, expected_batch)


if __name__ == "__main__":
    unittest.main()

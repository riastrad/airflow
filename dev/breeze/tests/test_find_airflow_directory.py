# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
from pathlib import Path
from unittest import mock

from airflow_breeze.utils.path_utils import AIRFLOW_SOURCES_ROOT, find_airflow_sources_root

ACTUAL_AIRFLOW_SOURCES = Path(__file__).parent.parent.parent.parent
ROOT_PATH = Path(Path(__file__).root)


def test_find_airflow_root_upwards_from_cwd(capsys):
    os.chdir(Path(__file__).parent)
    find_airflow_sources_root()
    assert ACTUAL_AIRFLOW_SOURCES == AIRFLOW_SOURCES_ROOT
    output = str(capsys.readouterr().out)
    assert output == ''


def test_find_airflow_root_upwards_from_file(capsys):
    os.chdir(Path(__file__).root)
    find_airflow_sources_root()
    assert ACTUAL_AIRFLOW_SOURCES == AIRFLOW_SOURCES_ROOT
    output = str(capsys.readouterr().out)
    assert output == ''


@mock.patch('airflow_breeze.utils.path_utils.AIRFLOW_CFG_FILE', "bad_name.cfg")
@mock.patch('airflow_breeze.utils.path_utils.Path.cwd')
def test_fallback_find_airflow_root(mock_cwd, capsys):
    mock_cwd.return_value = ROOT_PATH
    sources = find_airflow_sources_root()
    assert sources == ROOT_PATH
    output = str(capsys.readouterr().out)
    assert "Could not find Airflow sources" in output

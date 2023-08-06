# Copyright 2021 Edward Leardi. All Rights Reserved.
#
# Copyright 2020 IBM Corp. All Rights Reserved.
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
#

from pathlib import Path


def test_import_nourish_namespace():
    "Test to make sure top level public modules & subpackages are available in the global namespace."

    import nourish as test_nourish
    assert all(module.stem in dir(test_nourish) for module in Path('nourish').glob('[a-zA-Z]*'))


def test_import_nourish_loaders_namespace():
    "Test to make sure public modules are available in the loaders subpackage namespace."

    import nourish.loaders as test_nourish_loaders
    assert all(module.stem in dir(test_nourish_loaders) for module in Path('nourish/loaders').glob('[a-zA-Z]*'))

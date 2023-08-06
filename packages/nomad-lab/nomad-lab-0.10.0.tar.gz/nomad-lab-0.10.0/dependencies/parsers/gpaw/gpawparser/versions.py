#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
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

f2p_version = {6: '1.1.0',
               5: '0.11.0',
               3: '0.10.0'}


def get_prog_version(version):
    if isinstance(version, int):
        return f2p_version[version]
    else:
        return '0.9.0'


if __name__ == '__main__':
    print(get_prog_version(6))
    print(get_prog_version(0.3))

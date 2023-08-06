#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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

'''
The official NOMAD API.

There is a separate documentation for the API endpoints from a client perspective.

.. automodule:: nomad.app.flask.api.api
.. automodule:: nomad.app.flask.api.auth
.. automodule:: nomad.app.flask.api.upload
.. automodule:: nomad.app.flask.api.repo
.. automodule:: nomad.app.flask.api.archive
'''

from .api import api, blueprint
from . import info, auth, upload, repo, archive, encyclopedia, raw, mirror, dataset, metainfo

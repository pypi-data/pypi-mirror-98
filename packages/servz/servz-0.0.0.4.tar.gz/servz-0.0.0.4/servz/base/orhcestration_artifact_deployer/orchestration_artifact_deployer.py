# Copyright © 2020 Hashmap, Inc
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
from providah.factories.package_factory import PackageFactory as pf
import os

from servz.base.build_step import BuildStep
from servz.base.orhcestration_artifact_deployer.artifact_registries.artifact_registry import ArtifactRegistry
from servz.base.exceptions.deploy_script_generation_error import DeployScriptGenerationError


class OrchestrationArtifactDeployer(BuildStep):

    def __init__(self, **kwargs):
        super().__init__()
        self._workflow = list()
        reg_conf = kwargs.get('registry')
        self._registry: ArtifactRegistry = pf.create(key=reg_conf.get('type'), configuration=reg_conf.get('conf'))

    def build_part(self, **kwargs):

        _res = True
        for pipe in kwargs.get("artifact"):
            _res = _res and self._run(artifact=pipe['artifact_name'])
            self._registry.register(artifact=pipe['artifact_name'])
            os.remove(pipe['artifact_name'])

        if not _res:
            raise DeployScriptGenerationError()

        return True

    def _run(self, artifact: str):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def get_results(self):

        result = dict()
        if len(self._workflow) > 0:
            result = {
                "deployer": self._workflow
            }

        return result

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
from servz.base.build_step import BuildStep
from servz.base.exceptions.orchestration_artifact_build_error import OrchestrationArtifactBuildError


class OrchestrationArtifactBuilder(BuildStep):

    def __init__(self, **kwargs):
        super().__init__()
        self._workflows: list = list()

    def build_part(self, **kwargs):
        _res = self._build(pipelines=kwargs.get('packager'))

        if not _res:
            raise OrchestrationArtifactBuildError()
        return True

    def get_results(self):

        result = {
            "artifact": self._workflows
        }

        return result

    def _build(self, pipelines: list) -> bool:

        results = [self._compile_workflow(pipe) for pipe in pipelines]

        self._workflows = pipelines
        return all(wf['success'] for wf in results)

    def _compile_workflow(self, pipe):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    @classmethod
    def _generate_dependencies_string(cls, dependencies: list) -> str:
        if not dependencies:
            return ''

        return ','.join(dependencies)

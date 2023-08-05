# Modifications © 2020 Hashmap, Inc
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
import subprocess

from ml_builders.builders_and_generators.orhcestration_artifact_deployer.artifact_registries.artifact_registry import ArtifactRegistry


class GCSRegistry(ArtifactRegistry):

    def __init__(self, **kwargs):
        super().__init__()
        self.__path = kwargs.get('path')

    def register(self, artifact):
        subprocess.run(['gsutil', 'cp', artifact, self.__path], check=True, stderr=subprocess.STDOUT)

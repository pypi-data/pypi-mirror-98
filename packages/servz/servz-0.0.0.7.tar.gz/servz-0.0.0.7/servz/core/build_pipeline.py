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
from typing import NamedTuple

from servz.base.packager.packager import Packager
from servz.base.pipline_composer.pipeline_composer import PipelineComposer
from servz.base.workflow_validator.workflow_validator import WorkflowValidator


class BuildPipeline(NamedTuple):
    workflow_validator: WorkflowValidator
    pipeline_composer: PipelineComposer
    packager: Packager

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
import os
import yaml

from servz.base.pipline_composer.pipeline_composer import PipelineComposer
from servz.base.exceptions.pipeline_read_error import PipelineReadError


class YAMLPipelineComposer(PipelineComposer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__root_path = kwargs.get('project_path')
        self.__workflows_path = os.path.join(kwargs.get('project_path'), 'workflows')
        self._error_messages = []

    def _build(self, flows: dict) -> list:
        """
        Build and return a dict containing the information about all pipelines that will need to be built. The contents
        of the specification will be validated.

        Args:

            \
            flows: dictionary of all active flows

        Returns: flushed out pipeline flows as will be needed for building the containers

        """
        # Future Version will need to handle different schema versions via factory
        return [self.__build_flow(pipeline) for pipeline in flows['pipelines']]

    def __build_flow(self, pipeline: dict) -> None:

        # Read the pipeline yaml file
        pipeline_config_path = os.path.join(self.__workflows_path, 'pipelines', pipeline['name'] + '.yml')

        with open(pipeline_config_path, 'r') as fh:
            pipeline = yaml.safe_load(fh)

        self.__validate_pipeline(pipeline)

        if len(self._error_messages) > 0:
            self.__log_build_results()
            raise PipelineReadError("\n".join(self._error_messages))

        # get the workflow
        self._pipelines.append(pipeline)

    def __validate_pipeline(self, pipeline: dict) -> None:

        keys = [key.lower() for key in pipeline.keys()]
        required_keys = {'endpoints', 'version'}
        # Stages has root and workflow
        if not required_keys.intersection(keys):
            self._generate_validation_message(f'At least one of {required_keys} is missing from configuration.')

        endpoints: dict = pipeline.get('endpoints')
        # Endpoints is dict
        if not isinstance(endpoints, dict):
            self._generate_validation_message(f'"endpoints" must be a dict.')

        # Endpoints components are dicts
        if any([1 for node in endpoints if not isinstance(node, dict)]):
            self._generate_validation_message(f'All entries in the endpoints must be a dictionary.')

        # Endpoints component path and files exist and is a python file
        _ = [self.__validate_nodes(node=node) for node in endpoints]

    def __log_build_results(self) -> None:
        self._logger.error("\n".join(self._error_messages))

    def __validate_nodes(self, node: dict) -> None:

        keys = [key.lower() for key in node.keys()]
        if 'preprocess' not in keys:
            self._generate_validation_message("in Endpoints not 'preprocess' found.")

        if 'predict' not in keys:
            self._generate_validation_message("in Endpoints not 'predict' found.")

    def _generate_validation_message(self, message: str) -> None:
        return self._error_messages.append(f'In {__name__}: {message}')

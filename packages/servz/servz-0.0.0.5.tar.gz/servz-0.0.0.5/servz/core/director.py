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
import logging
import traceback
from servz.core.builder import Builder
from servz.base.exceptions.container_build_error import ContainerBuildError
from servz.base.exceptions.flow_build_error import FlowBuildError
from servz.base.exceptions.flow_validation_error import FlowValidationError


class Director:

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        # TODO Validate Builder steps are present

        # TODO This should be hidden in some way - maybe
        self._builder = Builder(**kwargs)

    def build_and_run(self) -> dict:
        """

        Returns:
            run summary as dict

        Raises:
            FlowValidationError

        """
        # ---------------------------- #
        # -------- Initialize -------- #
        # ---------------------------- #

        self._builder.build()

        run_summary = dict()

        try:

            self._builder.pipeline.workflow_validator.validate()

            self._builder.pipeline.pipeline_composer.build_part(**self._builder.pipeline.workflow_validator.get_results())

            self._builder.pipeline.packager.build_part(**self._builder.pipeline.pipeline_composer.get_results())

        except FlowValidationError:
            raise
        except FlowBuildError:
            raise
        except ContainerBuildError:
            raise
        except Exception:
            error_message = traceback.format_exc()
            self._error_handler(error_message)
            raise

        finally:
            self.__log_build_results(log_info=run_summary)

        # TODO: Summary needs to be built
        return run_summary

    def __log_build_results(self, log_info: dict) -> bool:
        pass

    def _error_handler(self, exception_message: str) -> None:
        error_message = f"Error occured in Source: {exception_message}"
        self._logger.exception(error_message)
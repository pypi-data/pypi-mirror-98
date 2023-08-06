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
import traceback
from jinja2 import Template
import uuid
from servz.packager.asset_bundler import AssetBundler
from servz.project_config import ProjectConfig


class FlaskBundler(AssetBundler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(kwargs,"---")
        self.__root_path: str = os.path.abspath(kwargs.get('project_path'))
        self.__prediction_main = ""
        self.__predictor = ''

    def build_runner_script(self, pipe):

        try:
            #  TODO:  template this out later
            runner = os.path.abspath(os.path.join(self.__root_path, 'server_' + uuid.uuid4().hex) + '.sh')
            requirements = 'pip install -r requirements_txt'
            executable_app = f'python app.py'
            # Save runner file to disk

            with open(runner, 'w') as fh:
                fh.write(requirements+"\n")
                fh.write(executable_app)
            fh.close()
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')

    def build_artifact_bundle(self, pipe):

        self.__prediction_main = pipe.get('predict')
        path = str(self.__prediction_main)
        path_list = ".".join(path.split('/'))
        self.__predictor = path_list.replace('.py', '')

    def build_endpoint(self, pipe):

        # read in template file
        flask_code_file = os.path.join(ProjectConfig.package_root(), 'server_templates', 'flask', 'app')
        with open(flask_code_file, 'r') as fh:
            code = fh.read()

        # apply parameters
        flask_code = Template(code, autoescape=True)
        endpoint = flask_code.render(predict=self.__predictor)

        # save out to local path
        server = os.path.abspath(os.path.join(self.__root_path, 'app.py'))
        print(server)
        with open(server, 'w') as fh:
            fh.write(endpoint)

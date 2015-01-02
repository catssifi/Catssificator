# Copyright (c) 2014 Ken Wu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# -----------------------------------------------------------------------------
#
# Author: Ken Wu
# Date: 2014 Dec - 2015

install_dir='./tmp_install_dir'
if [ ! -d "$install_dir" ]; then
	mkdir "$install_dir"
fi
cd "$install_dir"
wget https://pypi.python.org/packages/source/P/PyStemmer/PyStemmer-1.3.0.tar.gz
tar xvf PyStemmer-1.3.0.tar.gz
cd PyStemmer-1.3.0
python setup.py install
cd ..
wget http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz
tar xvf PyYAML-3.11.tar.gz
cd PyYAML-3.11
python setup.py install
cd ..
cd ..
rm -rf "$install_dir"
pip install tornado
# Copyright (c) 2015 Ken Wu
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

#This script is to populate the AI data (for the automatic sentence corrections/suggestions, user input syntax analysis..etc) to the system.  This can be running as a background thread parallel to the main server thread.  
#It can be repeatedly run 

echo "cd into $CLASSIFICATOR_HOME"
cd $CLASSIFICATOR_HOME

sudo ./src/maintenance/python/import_ai_data.py ./resources/ai/


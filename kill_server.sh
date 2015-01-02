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

n="$(ps -ef | grep -i "./src/main/python/start_catssificator_server.py" | grep -v grep | awk '{print $2}')"
if [[ -z "$n" ]];
then
	echo "Server was not started at all..."
else
	kill -9 "$n";
	echo "Server with pid: $n has been killed"
fi
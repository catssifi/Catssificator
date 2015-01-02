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
# Date: 2014 December
# 

get_json_value() {
	Received_Json_Value=`echo "$1" | 
python -c "
import json
import sys
json_data=sys.stdin.read()
decoded = json.loads(json_data)
print(decoded['"$2"'])
"`	
}

if [ $# -eq 1 ]; then

    curl_request=`curl -X POST http://127.0.0.1:9797/ -F query="$@" -s`
    get_json_value "$curl_request" "result"
    #echo "$Received_Json_Value"

    if [ "$Received_Json_Value" == "no" ]; then
        get_json_value "$curl_request" "message"
        echo "$Received_Json_Value"
        get_json_value "$curl_request" "ticket-token"
        ticket_token="$Received_Json_Value"
        while true; do
            read -p "Please enter a category number: " num
            case $num in
                [0-9]* )
                    curl_request=`curl -X POST http://127.0.0.1:9797/ -F ticket-token="$ticket_token" -F category="$num" -s`
                    echo "THANKS.  It has been recorded."; break;;
                * ) echo "Error!Please enter a number in above...";
            esac
        done

    else
        get_json_value "$curl_request" "category"
        echo "$Received_Json_Value"
    fi

elif [ $# -eq 2 ]; then

    curl_request=`curl -X POST http://127.0.0.1:9797/ -F query="$1" -F category="$2" -s`
    
else
    echo "Illegal number of arguments"
    exit 1
fi
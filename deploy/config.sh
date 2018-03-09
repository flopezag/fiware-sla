#!/usr/bin/env bash
##
# Copyright 2017 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##



# Initializing variables

PYTHON_FILE="SLAMeassurement.py"
INITIAL_HEADER="#\!\/usr\/bin\/env python"
FINAL_HEADER='#\!\/usr\/bin\/env '
VIRTUALENV_DIR='\/env\/bin\/python'

# 0) Changing the working directory to the parent directory.
cd ..

# 1) Install&Config virtualenv for User Create process
if [ ! -d "env" ]; then
  # Control will enter here if env does not exist.
  virtualenv -p python2.7 env

  source env/bin/activate
  pip install -r requirements.txt

  deactivate
fi



# 2) Configure SLAMeassurement.py file

working_directory=${PWD}

result=$(echo ${working_directory} | sed 's@/@\\/@g')

FINAL_HEADER=${FINAL_HEADER}${result}${VIRTUALENV_DIR}

sed -i -e "s/${INITIAL_HEADER}/${FINAL_HEADER}/" ${PYTHON_FILE}

chmod 744 ${PYTHON_FILE}



# 3) configure crontab
username="ubuntu"
result=$(crontab -u ${username} -l 2>/dev/null)

if [ "$result" == "" ]; then
    if [ -e /tmp/cronlock ]; then
        echo "cronjob locked"
        exit 1
    fi

    touch /tmp/cronlock

    echo "# FIWARE SLA process" | crontab -
    (crontab -u ${username} -l; echo "0 2 * * * "${working_directory}"/SLAMeassurement.py --noauth_local_webserver") | crontab -u ${username} -

    rm -f /tmp/cronlock

else
    crontab -u ${username} -l 2>/dev/null >a.out

    touch /tmp/cronlock

    line=$(grep "0 2 * * * "${working_directory}"/SLAMeassurement.py --noauth_local_webserver" a.out)
    if [ "$line" == "" ]; then
        (crontab -u ${username} -l; echo "") | crontab -
        (crontab -u ${username} -l; echo "# FIWARE SLA process") | crontab -
        (crontab -u ${username} -l; echo "0 2 * * * "${working_directory}"/SLAMeassurement.py --noauth_local_webserver") | crontab -u ${username} -
    fi

    rm -f /tmp/cronlock

    rm a.out
fi

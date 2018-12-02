# FIWARE Lab ticket resolution SLA

[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
<!-- [![Build Status](https://travis-ci.org/flopezag/fiware-sla.svg?branch=master)](https://travis-ci.org/flopezag/fiware-sla)
[![Coverage Status](https://coveralls.io/repos/github/flopezag/fiware-sla/badge.svg)](https://coveralls.io/github/flopezag/fiware-sla)
[![Documentation Status](https://readthedocs.org/projects/fiware-sla/badge/?version=latest)](http://fiware-sla.readthedocs.io/en/latest/?badge=latest)
-->

Management of FIWARE Lab nodes help-desk tickets SLA resolution timne.

* [Introduction](#introduction)
* [Overall description](#overall_description)
* [Build and Install](#build-and-install)
* [Running](#running)
* [Access to the historical information in Monasca](#Access_to_the_historical_information_in_Monasca)
* [Deployment](#deployment)
* [Testing](#testing)
* [Support](#support)
* [License](#license)

## Introduction

Python script to calculate the percentage of Help-Desk tickets responded and resolved per each
FIWARE Lab node in less than 24 working hours and less than 48 working hours.

## Overall description

The procedure to calculate this percentages is taking all the tickets resolved
since 1st January 2017 till now in [Jira](https://jira.fiware.org) under the
project Help-Desk and identified with the component FIWARE-LAB-HELP. This component
corresponds to the tickets that were created from the corresponding mail list
fiware-lab-help@lists.fiware.org.

Once that we have all the tickets, we categorized them into resolved and responded
and calculate the time in which they were resolved and responded. A ticket is responded
when the status of the ticket is moved from 'Open' to 'In Progress' or 'Answered'. A
ticket is resolved when it is moved from 'Close' status. The tickets that are dismissed
from 'Open' status are also taking into account in terms of calculate the progress time
of them.

Next step, once that we have the progressed time is calculate the different time. The process
is calculating the difference in working hours. It means that every day has only 9 hours
(from 8:00 to 17:00) to calculate the difference and weekends are not included. For example, if
a ticket was created on Friday 16/02/2018 at 9:35:24,43 and was resolved on Monday 19/02/2018
at 8:47:43,12 the resolution time will be difference time on friday until end of working day
plus the difference time from beginning of working day until the resolution time:

    16/02/2018: from 09:35:24,43 to 17:00:00,00 = 07:24:35,57
    19/02/2018: from 08:00:00,00 to 08:47:43,12 = 00:47:43,12

    TOTAL TIME: 07:24:35,57 + 00:47:43,12 = 08:12:18,69

Therefore the resolution time in that case was 8 hours, 12 minutes and 18,69 seconds. If the
ticket was created before 08:00:00, the starting point is considered 08:00:00. If the ticket is
closed after 17:00:00 it is considered closed at 17:00:00. In case of tickets created during
weekends, the created time is the next Monday at 08:00:00. In case of tickets closed during
weekends, the closed time is the previous Friday at 17:00:00.

In this process is not considered bank holidays for each region.

Once that we have the response and resolution times we send the information to the
[OpenStack Monasca](https://wiki.openstack.org/wiki/Monasca) instance in order to keep centralized
the monitoring information and make afterwards if could be necessary some type of statistical
analysis. For this purpose we store also the number of tickets for each region. Keep in mind,
that it is needed a request to [OpenStack Keystone](https://wiki.openstack.org/wiki/Keystone)
service in order to recover a proper token in order to send the information to the 
[Monasca API](https://github.com/openstack/monasca-api/blob/master/docs/monasca-api-spec.md). 
In that case we are using the tenant name service due to the Monasca instance is configured to 
pass the monitoring information under this tenant.

## Build and Install

### Requirements

The following software must be installed:

* Python 2.7
* pip
* virtualenv

### Installation

The recommend installation method is using a virtualenv. Actually, the
installation process is only about the python dependencies, because the python
code do not need installation.

1. Clone this repository.
1. Define the configuration file in './config/fiware-sla.ini'
1. Execute the script 'source ./deploy/config.sh'.
1. With root user, execute the command 'cp ./config/fiware-sla.logrotate /etc/logrotate.d/fiware-sla'.

## Running

Once that you have installed and configured your application, you can run it
just executing:

    python SLAMeassurement.py

And it will be executed in order to calculate the corresponding SLA levels for all the nodes and
send the information to the configured Monasca interface. Keep in mind that you have to be inside
a previously defined virtual environment.

The ``config.sh`` file that you can find in the [deploy](deploy) folder is used in order to allow
the automatic execution of the python script just adding the corresponding header to the file
SLAMeassurement.py:

    #!/usr/bin/env /env/bin/python

Where env is the name of your virtual environment.

Last but not least, the service is added into the
[crontab](https://manpages.debian.org/jessie/cron/crontab.5.en.html) of the machine in order to
execute the service every day at 02:00:00.

## Access to the historical information in Monasca

The service is configured in order to send the data to the [FIWARE OpenStack Monasca](monasca.lab.fiware.org)
service in order to keep a historical information about the resolution of the tickets. You can check those
measurements directly over the Monasca API but previously it is required to obtain a secure token
associated to the Ceilometer service requesting it to the Keystone instance:

```console
curl -X POST   http://cloud.lab.fiware.org:4730/v2.0/tokens  \
     -H 'Accept: application/json'   \
     -H 'Content-Type: application/json'   \
     -d '{
    "auth": {
        "tenantName": "service",
        "passwordCredentials": {
            "username": "<ceilometer service user, one per region>",
            "password": "<ceilometer service user password>"
        }
    }
}' | jq .access.token.id
```

If you do not have installed the [jq tool](https://stedolan.github.io/jq/), please download it in order to navigate
inside the json response and obtain the proper token id in a easy way.

Now, it is time to remember how is managed the metrics inside Monasca. In order to send the data
we have defined two dimensions in Monasca:

* metric: a metric name to filter metrics by. By default we have defined the metrics region.ticket_resolve_time
  and region.ticket_response_time for the percentage of resolve and response of the Help-Desk associated to each
  region. You can obtain this data also requesting to Monasca API:

  ```console
  curl -X GET   http://monasca.lab.fiware.org:8070/v2.0/metrics/names   \
       -H 'Cache-Control: no-cache'   \
       -H 'X-Auth-Token: <Ceilometer service token>' | jq .elements[].name
  ```

* source: the application that provide this SLA data, in our case it is fixed to fiware-sla
* region: this is the region name in which we calculate the values of SLA. You can request the list of available 
  regions directly to Monasca through the execution of the following query:

  ```console
  curl -X GET   'http://monasca.lab.fiware.org:8070/v2.0/metrics?name=region.ticket_resolve_time'   \
       -H 'Cache-Control: no-cache'   \
       -H 'X-Auth-Token: <Ceilometer service token>' | jq .elements[].dimensions.region
  ```

Now to request the measurements associated to the ticket resolve time in the Spain region starting at 15/08/2018
just execute the following query:

```console
curl -X GET   'http://monasca.lab.fiware.org:8070/v2.0/metrics/measurements?name=region.ticket_resolve_time&start_time=2018-08-15T00:00:01Z&dimensions=region:Spain'   \
     -H 'Cache-Control: no-cache'   \
     -H 'X-Auth-Token: <Ceilometer service token>' | jq
```

If you want to get more details about the use of OpenStack Monasca API, please take a look to the official
documentation about it in [monasca-api](https://github.com/openstack/monasca-api).

## Deployment

There is a specific option to deploy this service in a host. Take a look to
the content of [deploy](deploy/README.md) directory

## Testing

### Unit Tests

It was defined a minimum set of tests to cover the core functionality of the
service. The ``tests`` target is used for running the unit tests in the
component. We use for those tests the tox tool.
[Tox](https://tox.readthedocs.io/en/latest/) is a generic
[virtualenv](https://pypi.python.org/pypi/virtualenv) management and test
command line tool you can use for checking your package installs correctly
with different Python versions and interpreters running your tests in each
of the environments, configuring your test tool of choice acting as a
frontend to Continuous Integration servers, greatly reducing boilerplate and
merging CI and shell-based testing.

The configuration file can be found in ``tox.ini`` in which we have defined two
different environments:

* The first one, to test the service using [nosetests](http://nose.readthedocs.io/en/latest/).
* The second one, to check the python coding style using [pycodestyle](https://pycodestyle.readthedocs.io/en/latest/)

First of all, you need to install the tool with the following commands:

    pip install tox

Now, you can run the tests, simply execute the commands:

    tox

## Support

The support of this service is under github. You can create your [issues](https://github.com/flopezag/fiware-sla/issues/new)
and they will be resolved by the development team in the following sprint.

## License

\(c) 2018 FIWARE Foundation, e.V., Apache License 2.0

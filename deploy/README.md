# Setting up a stand-alone FIWARE Lab User Create service

This content describes how to deploy FIWARE SLA service using an
[ansible](http://www.ansible.com) playbook. It has been tested on the
[FIWARE Lab](https://cloud.lab.fiware.org) cloud.

It will install the service and the different configurations file in order
to calculate automatically the SLA levels associated to the response and
resolution of the JIRA tickets associates to each FIWARE Lab node.

Additionally, it autoconfigures the tool in order to use it every day through
the configuration of the proper crontab service.

## How to start it

* Create virtualenv and activate it:

      virtualenv -p python2.7 $NAME_VIRTUAL_ENV
      source $NAME_VIRTUAL_ENV/bin/activate

* Install the requirements:

      pip install -r requirements.txt

* Edit the setup variables to fit your setup. Open `vars/data.yml` and setup
  the variables as explained there.

* One all the variables are in place you should now be able to deploy and
  configure the service. Just run the following command:

      ansible-playbook -vvvv -i inventory.yml \
      --private-key=(Key pair to access to the instance) \
      deploy_fiwaresla.yml

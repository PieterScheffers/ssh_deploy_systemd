#!/usr/bin/env python

## Set this script as default shell for a user
# useradd -m -s /path/to/this/deploy.py myuser

## Give user no password sudo rights
# Add to /etc/sudoers:
# deployer ALL=(ALL) !ALL
# deployer ALL=NOPASSWD: /bin/systemctl

## Call via ssh with service to restart
# ssh myuser@myhost myapp.service

import sys
from os.path import expanduser, join
from subprocess import check_call, STDOUT, Popen, PIPE, call

# Find all services on the system
def find_services():
    # sudo systemctl list-units --all | grep .service | awk '{print $1$2}'

    proc = Popen([ 'sudo', 'systemctl', 'list-units', '--all' ], stdout=PIPE, stderr=PIPE)
    out = proc.stdout.read()

    # split by word, check if word endswith .service, create a list of it
    services = [ w for w in out.split() if w.endswith('.service') ]

    return services

def restart_service(service):
    try:
        check_call([ 'sudo', 'systemctl', 'restart', service ]) # raises a CalledProcessError if return code isn't 0
    except CalledProcessError as e:
        sys.exit(e.strerror)

# Read the ~/.valid_services file for services allowed to restart
def read_valid_services():
    try:
        path = join(expanduser("~"), '.valid_services')
        file = open(path, 'r')  # raises a IOError if file doesn't exist
        contents = file.read()
        return contents.split()
    except IOError as e:
        sys.exit(e.strerror)

    return []



# script arguments
#   0: <scriptname>
#   1: -c
#   2: sudo systemctl start bla.service

if len(sys.argv) < 3:
    sys.exit("Should have at least 3 arguments")

[ script, c, service ] = sys.argv

if c != '-c':
    sys.exit("ssh should run a command")

if not service.endswith('.service'):
    sys.exit("command should be a service")

if not service in read_valid_services():
    sys.exit("Service not allowed")

if not service in find_services():
    sys.exit("Service should exist")

print "(Re)Starting", service
restart_service(service)


# print 'Number of arguments: ' + str(len(sys.argv)) + ' arguments.'
# print 'Argument List: ' + str(sys.argv)




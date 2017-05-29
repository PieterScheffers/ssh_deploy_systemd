#!/usr/bin/env bash

# Create deployer user
useradd \ 
-s /docker/projects/deploy-shell/deploy.py \ # set shell
-m \ # create HOME
myuser

# Add deployer user to sudo without password for /bin/systemctl
echo "deployer ALL=(ALL) !ALL" >> /etc/sudoers
echo "deployer ALL=NOPASSWD: /bin/systemctl" >> /etc/sudoers

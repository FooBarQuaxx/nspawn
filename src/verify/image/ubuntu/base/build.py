#!/usr/bin/env python

import os, runpy
this_dir = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(f"{this_dir}/a.py")

from nspawn.build import *

name = "bionic"
version = "18.04"
image_url = f"file://localhost/tmp/nspawn/repo/ubuntu/base/{name}-{version}.tar.gz"
booter_url = f"https://cloud-images.ubuntu.com/minimal/releases/{name}/release/ubuntu-{version}-minimal-cloudimg-amd64-root.tar.xz"

# declare image identity
IMAGE(image_url)

# provision dependency image
PULL(booter_url)

# configure container profile
WITH(
    Boot="yes",  # auto-find image init program
    Quiet="yes",  # suppress "press to escape" message
    KeepUnit="yes",  # use service unit as nspawn scope
    Register="yes",  # expose service unit with machinectl
)

# copy local resources
COPY("/etc")
COPY(path="/root")

SH("rm -rf /etc/resolv.conf /etc/securetty")

SH("apt-get update")
SH("apt-get install -y mc htop")
SH("apt-get install -y iputils-ping iproute2")
SH("apt-get install -y openssh-server")
SH("apt-get purge -y unattended-upgrades")
SH("systemctl disable networkd-dispatcher")
SH("systemctl enable systemd-networkd")
SH("systemctl enable systemd-resolved")
SH("systemctl enable ssh")

# publish image
PUSH()

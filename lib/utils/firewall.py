# -*- encoding: utf-8 -*-

import os

def dropIncomingPacketsFromHost(host):
    os.system("iptables -I INPUT -s %s -j DROP" % host);


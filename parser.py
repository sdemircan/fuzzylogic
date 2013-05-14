#-*- encoding: utf-8 -*-
#!/usr/bin/python

#imports standart library
import sys
import re

#import third party modules
import tailer
from logsparser import lognormalizer
from threading import Timer, Thread
import datetime
import time

class Pattern:
    def __init__(self, program):
        if (program == "apache"):
            self.pattern = self.get_apache_log_pattern()


    def get_apache_log_pattern(self):
        # this pattern to parse apache access log
        pattern_re = [
                       r'(?P<host>\S+)',                   # host %h
                       r'\S+',                             # indent %l (unused)
                       r'(?P<user>\S+)',                   # user %u
                       r'\[(?P<time>.+)\]',                # time %t
                       r'"(?P<request>.+)"',               # request "%r"
                       r'(?P<status>[0-9]+)',              # status %>s
                       r'(?P<size>\S+)',                   # size %b (careful, can be '-')
                       r'"(?P<referer>.*)"',               # referer "%{Referer}i"
                       r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
                      ]
        pattern = re.compile(r'\s+'.join(pattern_re)+r'\s*\Z')
        return pattern


class Parser(Thread):
    def __init__(self, log_path):
        super(Parser, self).__init__()
        self.hosts = {}    
        self.parserFile = log_path
        self.lognorm = lognormalizer.LogNormalizer('/home/serhat/İndirilenler/pylogsparser-0.8/normalizers')

    def parse(self, logline):
        log = {'raw' : logline}
        startTime = time.time()
        self.lognorm.lognormalize(log)
        
        self.pattern = Pattern("apache")
        #apache_line = log['raw'].split(":",3)[-1].lstrip()
        matched = self.pattern.pattern.match(log['raw'])
        if matched:
            information = matched.groupdict()
            if self.hosts.has_key(information['host']):
                self.hosts[information['host']]['count'] += 1
                self.hosts[information['host']]['lastUpdated'] = startTime
            else:
                self.hosts[information['host']] = {}
                self.hosts[information['host']]['count'] = 1
                self.hosts[information['host']]['startTime'] = startTime
                self.hosts[information['host']]['lastUpdated'] = startTime
   
    def getHosts(self):
        return hosts

    def run(self):
        for logline in tailer.follow(open(self.parserFile)):
            self.parse(logline)



if __name__ == "__main__":
    parser = Parser("/var/log/apache2/access.log")
    parser.start()

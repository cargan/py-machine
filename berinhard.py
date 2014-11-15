#!/usr/bin/python

import sys, getopt #command line tools
import psutil, subprocess #memory and disk
from time import strftime #atetime #data
import feedparser #rss

class CommandManager(object):
    command = None
    _actions = set(['system_stats', 'dummy', 'news_headlines'])

    def __init__(self, *args, **kwargs):
        self.command = kwargs.get('command')
        if self.command == None:
            raise Exception('command not provided')
        if not self.command in self._actions:
            raise Exception('command %s does not exists' % self.command)

    def perform(self):
        getattr(self, self.command)()

    def _get_memory_usage(self):
        return psutil.phymem_usage()

    def _get_disk_usage(self):
        df = subprocess.Popen(["df", "berinhard.py"], stdout=subprocess.PIPE)
        output = df.communicate()[0]
        return output

    def system_stats(self):
        print 'SYSTEM STATS OUTPUT'
        print 'DATE', strftime('%Y-%m-%d %H:%M:%S')
        print 'MEMORY USAGE: ', self._get_memory_usage()
        print 'DISK USAGE: ', self._get_disk_usage()

    def news_headlines(self):
        feed = feedparser.parse('feed://www.delfi.lt/rss/feeds/lithuania.xml')
        for entry in feed['entries']:
            print entry['title'], "\n", entry['summary'], "\n\n"



def main(argv):
    command = None
    try:
        opts, args = getopt.getopt(argv,"hc:",["inputCommand"])
    except getopt.GetoptError:
        print 'test.py -c <command>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -c <inputCommand>'
            sys.exit()
        elif opt in ("-c", "--inputCommand"):
            command = arg

    CManager = CommandManager(command=command)
    CManager.perform()

if __name__ == "__main__":
    main(sys.argv[1:])



import os
import sys

from .monitor import Monitor

class ContextSwitchesParser:
    def __init__(self, pid, dataAggregator):
        self.pid = pid
        self.dataAggregator = dataAggregator
        self.dataAggregator.addGaugeType('voluntary_ctxt_switches')
        self.dataAggregator.addGaugeType('nonvoluntary_ctxt_switches')

    def fetchData(self, timestamp, verbose):
        try:
            with open(os.path.join('/proc/', self.pid, 'status'), 'r') as pidfile:
                lines = pidfile.readlines()
                for line in lines:
                    if line.startswith('voluntary_ctxt_switches:'):
                        self.voluntary_ctxt_switches = line.split(':')[1].strip()
                        self.dataAggregator.record('voluntary_ctxt_switches', 
                            self.voluntary_ctxt_switches, timestamp, verbose)
                    if line.startswith('nonvoluntary_ctxt_switches:'):
                        self.nonvoluntary_ctxt_switches = line.split(':')[1].strip()
                        self.dataAggregator.record('nonvoluntary_ctxt_switches', 
                            self.nonvoluntary_ctxt_switches, timestamp, verbose)
        except IOError as e:
            print('ERROR: %s' % e)
            sys.exit(2)


class ContextSwitchesMonitor(Monitor):
    def __init__(self, pid, dataAggregator):
        super().__init__(pid, ContextSwitchesParser(pid, dataAggregator), dataAggregator)

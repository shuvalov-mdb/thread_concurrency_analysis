import os
import sys

from .monitor import Monitor

class ContextSwitchesParser:
    def __init__(self, pid, dataAggregator):
        self.pid = pid
        self.dataAggregator = dataAggregator
        self.dataAggregator.addRateType('voluntary_ctxt_switches')
        self.dataAggregator.addRateType('nonvoluntary_ctxt_switches')

    def fetchData(self, timestamp, verbose):
        try:
            with open(os.path.join('/proc/', self.pid, 'status'), 'r') as pidfile:
                lines = pidfile.readlines()
                for line in lines:
                    if line.startswith('voluntary_ctxt_switches:'):
                        self.voluntary_ctxt_switches = int(line.split(':')[1].strip())
                        self.dataAggregator.record('voluntary_ctxt_switches', 
                            self.voluntary_ctxt_switches, timestamp, verbose)
                    if line.startswith('nonvoluntary_ctxt_switches:'):
                        self.nonvoluntary_ctxt_switches = int(line.split(':')[1].strip())
                        self.dataAggregator.record('nonvoluntary_ctxt_switches', 
                            self.nonvoluntary_ctxt_switches, timestamp, verbose)
        except IOError as e:
            print('ERROR: %s' % e)
            sys.exit(2)


class ContextSwitchesMonitor(Monitor):
    def __init__(self, pid, dataAggregator):
        super().__init__(pid, ContextSwitchesParser(pid, dataAggregator), dataAggregator)


# Captures scheduler stats.
# Please not that CPU stats are no longer in jiffies bu in nanoseconds:
#   https://unix.stackexchange.com/questions/418773/measure-units-in-proc-pid-schedstat
class SchedStatParser:
    def __init__(self, pid, dataAggregator):
        self.pid = pid
        self.dataAggregator = dataAggregator
        self.dataAggregator.addTimeRateType('cpu_time')
        self.dataAggregator.addTimeRateType('run_queue_time')

    def fetchData(self, timestamp, verbose):
        try:
            with open(os.path.join('/proc/', self.pid, 'schedstat'), 'r') as pidfile:
                lines = pidfile.readlines()
                for line in lines:
                    data = line.split(' ')
                    self.cpu_time = int(data[0].strip())
                    self.run_queue_time = int(data[1].strip())
                    self.dataAggregator.record('cpu_time', 
                        self.cpu_time, timestamp, verbose)
                    self.dataAggregator.record('run_queue_time', 
                        self.run_queue_time, timestamp, verbose)
        except IOError as e:
            print('ERROR: %s' % e)
            sys.exit(2)

class SchedStatMonitor(Monitor):
    def __init__(self, pid, dataAggregator):
        super().__init__(pid, SchedStatParser(pid, dataAggregator), dataAggregator)


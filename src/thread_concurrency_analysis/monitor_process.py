import argparse
from datetime import datetime

from .proc_parsers import ContextSwitchesMonitor
from .data_aggregator import DataAggregator

class MonitorAggregator:
    def __init__(self, pid):
        self.monitors = []
        self.pid = pid
        self.dataAggregator = DataAggregator()
        self.monitors.append(ContextSwitchesMonitor(pid, self.dataAggregator))

    def oneCycle(self):
        dt = datetime.now()
        for monitor in self.monitors:
            monitor.fetch(dt)

def monitor_process_main():
  
    parser = argparse.ArgumentParser(prog ='monitor-process-concurrency',
                                     description ='Monitor process concurrency.')
  
    parser.add_argument('--pid',
                        help ="<pid> of the process to monitor.")
  
    args = parser.parse_args()
  
    if args.pid is None:
        print("Arg --pid is required")
        exit(1)

    aggregator = MonitorAggregator(args.pid)
    aggregator.oneCycle()

if __name__ == '__main__':
    monitor_process_main()


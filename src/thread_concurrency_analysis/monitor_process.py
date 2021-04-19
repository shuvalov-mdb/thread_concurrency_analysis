import argparse
import time
from datetime import datetime

from .proc_parsers import ContextSwitchesMonitor
from .proc_parsers import SchedStatMonitor
from .data_aggregator import DataAggregator
from .renderer import Renderer

class MonitorAggregator:
    def __init__(self, pid, filename, verbose):
        self.monitors = []
        self.pid = pid
        self.dataAggregator = DataAggregator(Renderer(filename), verbose)
        self.monitors.append(ContextSwitchesMonitor(pid, self.dataAggregator))
        self.monitors.append(SchedStatMonitor(pid, self.dataAggregator))
        self.dataAggregator.outputHeader()
        self.verbose = verbose

    def oneCycle(self):
        dt = datetime.now()
        for monitor in self.monitors:
            monitor.fetch(dt, self.verbose)
        self.dataAggregator.renderLine(dt)

    def close(self):
        self.dataAggregator.close()

def monitor_process_main():
  
    parser = argparse.ArgumentParser(prog ='monitor-process-concurrency',
                                     description ='Monitor process concurrency.')
  
    parser.add_argument('--pid',
                        help ="<pid> of the process to monitor.")
    parser.add_argument('--file',
                        help ="output file.")
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
  
    args = parser.parse_args()
  
    if args.pid is None:
        print("Arg --pid is required")
        exit(1)

    filename = "/tmp/concurrency_stats.txt"
    if args.file is not None:
        filename = args.file
    print('Output file: ', filename)

    if args.verbose:
        print("Enable verbose")

    aggregator = MonitorAggregator(args.pid, filename, args.verbose)

    try:
        while True:
            aggregator.oneCycle()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Interrupted')
    aggregator.close()

if __name__ == '__main__':
    monitor_process_main()


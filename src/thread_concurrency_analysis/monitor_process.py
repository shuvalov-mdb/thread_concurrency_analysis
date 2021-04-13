import argparse
import time
from datetime import datetime

from .proc_parsers import ContextSwitchesMonitor
from .data_aggregator import DataAggregator
from .renderer import Renderer

class MonitorAggregator:
    def __init__(self, pid, filename, verbose):
        self.monitors = []
        self.pid = pid
        self.dataAggregator = DataAggregator(Renderer(filename))
        self.monitors.append(ContextSwitchesMonitor(pid, self.dataAggregator))
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
    parser.add_argument('-verbose',
                        help ="verbose.")
  
    args = parser.parse_args()
  
    if args.pid is None:
        print("Arg --pid is required")
        exit(1)

    filename = "/tmp/concurrency_stats.txt"
    if args.file is not None:
        filename = args.file
    print('Output file: ', filename)

    if args.verbose is None:
        args.verbose = False

    aggregator = MonitorAggregator(args.pid, filename, args.verbose)
    aggregator.oneCycle()
    time.sleep(1)
    aggregator.oneCycle()
    aggregator.close()

if __name__ == '__main__':
    monitor_process_main()


import sys
from datetime import timedelta

# This data type is for events per unit of time, the calculation produces QPS.
class Rate:
    def __init__(self, verbose):
        self.verbose = verbose
        self.lastTimestamp = None
        self.lastData = None
        self.calculatedRate = 0.

    def record(self, data, timestamp, name):
        if self.lastTimestamp is not None:
            timeDiffUs = (timestamp - self.lastTimestamp) / timedelta(microseconds=1)
            dataDiff = data - self.lastData
            self.calculatedRate = (1000. * dataDiff) / (timeDiffUs / 1000.)
            if self.verbose:
                print(f"Rate for {name}: {dataDiff} ({self.lastData} -> {data}) in " +
                    f"{timeDiffUs / 1000000.} sec at {timestamp}")
        self.lastTimestamp = timestamp
        self.lastData = data

    def data(self):
        return self.calculatedRate

# Similar to rate, only the data is the rate of timeslices expressed in nanoseconds.
# Example of data is run queue from /proc/<pid>/schedstat.
class TimeRate:
    def __init__(self, verbose):
        self.verbose = verbose
        self.lastTimestamp = None
        self.lastData = None
        self.calculatedRate = 0.

    def record(self, data, timestamp, name):
        if self.lastTimestamp is not None:
            timeDiffUs = (timestamp - self.lastTimestamp) / timedelta(microseconds=1)
            dataDiff = data - self.lastData
            self.calculatedRate = (dataDiff / 1000.) / timeDiffUs
            if self.verbose:
                print(f"Rate for {name}: {dataDiff} ({self.lastData} -> {data}) in " +
                    f"{timeDiffUs / 1000000.} sec at {timestamp}")
        self.lastTimestamp = timestamp
        self.lastData = data

    def data(self):
        return self.calculatedRate

class Gauge:
    def __init__(self, verbose):
        self.verbose = verbose
        self.gauge = 0.

    def record(self, data, timestamp, name):
        self.lastTimestamp = timestamp
        self.gauge = data
        if self.verbose or True:
            print(f"Gauge for {name}: {data}")

    def data(self):
        return self.gauge

class DataAggregator:
    def __init__(self, renderer, verbose):
        self.metrics = {}
        self.renderer = renderer
        self.verbose = verbose
        self.keys = []

    def addRateType(self, name):
        self.metrics[name] = Rate(self.verbose)

    def addTimeRateType(self, name):
        self.metrics[name] = TimeRate(self.verbose)

    def addGaugeType(self, name):
        self.metrics[name] = Gauge(self.verbose)

    def outputHeader(self):
        self.keys = self.metrics.keys()
        self.renderer.renderHeader(self.keys)

    def record(self, name, data, timestamp, verbose):
        metric = self.metrics.get(name)
        if metric is None:
            print('Unexpected metric ', name)
            sys.exit(2)
        metric.record(data, timestamp, name)

    def renderLine(self, timestamp):
        data = []
        for key in self.keys:
            metric = self.metrics.get(key)
            data.append(metric.data())
        self.renderer.renderData(timestamp, data)

    def close(self):
        self.renderer.close()

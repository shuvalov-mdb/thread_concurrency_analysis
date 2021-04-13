import sys

class Rate:
    def __init__(self):
        self.lastTimestamp = None
        self.lastData = None
        self.calculatedRate = 0.

    def record(self, data, timestamp):
        if self.lastTimestamp is not None:
            timeDiffUs = timestamp.microsecond - self.lastTimestamp.microsecond
            dataDiff = data - self.lastData
            self.calculatedRate = (1000. * dataDiff) / (timeDiffUs / 1000.)
        self.lastTimestamp = timestamp
        self.lastData = data

    def data(self):
        return self.calculatedRate

class Gauge:
    def __init__(self):
        self.gauge = 0.

    def record(self, data, timestamp):
        self.lastTimestamp = timestamp
        self.gauge = data

    def data(self):
        return self.gauge

class DataAggregator:
    def __init__(self, renderer):
        self.metrics = {}
        self.renderer = renderer
        self.keys = []

    def addRateType(self, name):
        self.metrics[name] = Rate()

    def addGaugeType(self, name):
        self.metrics[name] = Gauge()

    def outputHeader(self):
        self.keys = self.metrics.keys()
        self.renderer.renderHeader(self.keys)

    def record(self, name, data, timestamp, verbose):
        metric = self.metrics.get(name)
        if metric is None:
            print('Unexpected metric ', name)
            sys.exit(2)
        metric.record(data, timestamp)

    def renderLine(self, timestamp):
        data = []
        for key in self.keys:
            metric = self.metrics.get(key)
            data.append(metric.data())
        self.renderer.renderData(timestamp, data)

    def close(self):
        self.renderer.close()

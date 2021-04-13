
class Rate:
    def __init__(self):
        pass

class Gauge:
    def __init__(self):
        pass

class DataAggregator:
    def __init__(self):
        self.metrics = {}

    def addRateType(self, name):
        self.metrics[name] = Rate()

    def addGaugeType(self, name):
        self.metrics[name] = Gauge()

    def record(self, name, data, timestamp):
        metric = self.metrics.get(name)
        if metric is None:
            print('Unexpected metric ', name)
            sys.exit(2)


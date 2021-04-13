

class Monitor:
    def __init__(self, pid, parser, dataAggregator):
        self.pid = pid
        self.parser = parser
        self.dataAggregator = dataAggregator

    def fetch(self, timestamp, verbose):
        self.parser.fetchData(timestamp, verbose)
        

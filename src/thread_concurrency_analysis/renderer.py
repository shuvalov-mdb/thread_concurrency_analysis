

class Renderer:
    def __init__(self, filename):
        self.file = open(filename,"w")

    def renderHeader(self, keys):
        self.file.write("# time ")
        for key in keys:
            self.file.write(key)
            self.file.write(" ")
        self.file.write("\n")

    def renderData(self, timestamp, dataArray):
        self.file.write(timestamp.isoformat())
        self.file.write(" ")
        for data in dataArray:
            self.file.write(str(data))
            self.file.write(" ")
        self.file.write("\n")

    def close(self):
        self.file.close()


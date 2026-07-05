class NewtonRing:
    def __init__(self, data, radius, start=5):
        self.diameter_data = data
        self.pixel_data = []
        self.real_data = []
        self.radius = radius
        self.k_list = []
        self.dt = None                # pixel/mm(visio)
        self.get_dt()
        self.getPixelData()
        self.get_k_list(start)

    def get_dt(self):
        visio_size = (169.333, 127)     # mm
        orig_size = (640, 480)          # pixel

        self.dt = (orig_size[0]/visio_size[0] + orig_size[1]/visio_size[1])/2

        return self.dt

    def getPixelData(self):
        self.pixel_data = []
        for diameter in self.diameter_data:
            self.pixel_data.append(diameter * self.dt)

        return self.pixel_data

    def get_k_list(self, start):
        self.k_list = [start + i for i in range(0, len(self.diameter_data))]
        return self.k_list

    def getRealData(self, dx):
        self.real_data = []
        for diameter in self.pixel_data:
            self.real_data.append(diameter * dx)

        return self.real_data


# unit: mm(visio)
data1 = [77.36, 83.068, 88.211, 93.139, 97.625, 102.172, 106.361, 110.419, 114.423, 118.486]
Newton_850 = NewtonRing(data1, 850)

data2 = [80.562, 87.22, 92.549, 98.281, 103.354, 108.574, 113.566, 118.178, 122.276, 126.548]
Newton_1000 = NewtonRing(data2, 1000)

data3 = [92.007, 100.06, 107.338, 113.815, 120.044, 126.847, 131.975, 137.271, 142.982, 148.156]
Newton_1432 = NewtonRing(data3, 1432)

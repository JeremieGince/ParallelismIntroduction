class Sensor:
	rawData = "./data/archive/austin_weather.csv"

	def __init__(self, sensor_id: int, name: str, units: str = '-'):
		self.sensor_id = sensor_id
		self.name = name
		self.units = units
		self._date = None

	@property
	def columns_names(self):
		raise NotImplementedError()

	def set_date(self, date):
		self._date = date

	def read(self):
		raise NotImplementedError()

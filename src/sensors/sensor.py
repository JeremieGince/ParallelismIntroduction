

class Sensor:
	def __init__(self, sensor_id: int, name: str):
		self.sensor_id = sensor_id
		self.name = name
		self._date = None

	def set_date(self, date):
		self._date = date

	def read(self):
		raise NotImplementedError()




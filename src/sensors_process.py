import multiprocessing as mp

from .sensor_loggers import SensorLogger


class SensorsProcess(mp.Process):
	def __init__(self, sensors, lock, date):
		super().__init__()
		self.sensors = sensors
		self.lock = lock
		self.date = date
		self.exit_event = mp.Event()

	def run(self):
		sensor_loggers = [SensorLogger(sensor, self.lock) for sensor in self.sensors]
		for logger in sensor_loggers:
			logger.set_date(self.date)
			logger.start()
		self.exit_event.wait()
		for logger in sensor_loggers:
			logger.join()

	def join(self, timeout=None):
		self.exit_event.set()
		super(SensorsProcess, self).join(timeout)

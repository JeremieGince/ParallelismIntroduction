import multiprocessing as mp
import time
import typing

from .sensors.sensor import Sensor
from src.weather_predictor.weather_predictor import WeatherPredictor
from .sensors_process import SensorsProcess


class App:
	def __init__(self, sensors: typing.List[Sensor], seconds_per_day: int = 100_000):
		self.sensors = sensors
		self.sensors_lock = mp.RLock()
		self.weather_predictor = WeatherPredictor(self.sensors_lock)
		self.seconds_per_day = seconds_per_day
		self.done_date = list()
		self.sensors_process = None

	def run(self, n_day='all'):
		raise NotImplementedError()

	def run_single_day(self, date):
		print(f"Start day - {date}")
		self.start_day(date)
		time.sleep(self.seconds_per_day)
		print(f"Stop day - {date}")
		self.stop_day(date)

	def start_day(self, date):
		"""
		run start_sensors and start_predictor in multiprocessing
		:param date:
		:return:
		"""
		self.sensors_process = SensorsProcess(self.sensors, self.sensors_lock, date)
		self.sensors_process.start()

	def stop_day(self, date):
		self.done_date.append(date)
		self.stop_processes()

	def stop_processes(self):
		self.sensors_process.join()
		self.sensors_process.kill()
		self.sensors_process.close()

	def start_predictor(self, date):
		"""
		#TODO:
		- read and add the data of the previous day to the training set.
		- re-train the model.
		-

		:param date:
		:return:
		"""
		# self.weather_predictor.set_date(date)
		# self.weather_predictor.set_done_date(self.done_date)
		# self.weather_predictor.run()
		pass

	def log_sensor_data(self, sensor):
		pass

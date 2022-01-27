import multiprocessing as mp
import time
import typing
from threading import Thread

from sensor_loggers import SensorLogger
from sensors.sensor import Sensor


class App:
	def __init__(self, sensors: typing.List[Sensor], seconds_per_day: int = 100_000):
		self.sensors = sensors
		self.sensor_loggers = [SensorLogger.new(sensor) for sensor in sensors]
		self.seconds_per_day = seconds_per_day
		self.done_date = []
		self.logger_to_thread = {}
		self.processes = {}

	def run(self, n_day='all'):
		raise NotImplementedError()

	def run_single_day(self, date):
		self.start_day(date)
		time.sleep(self.seconds_per_day)
		self.stop_day(date)

	def start_day(self, date):
		"""
		run start_sensors and start_predictor in multiprocessing
		:param date:
		:return:
		"""
		self.processes["sensors"] = mp.Process(target=self.start_sensors, args=(date,))
		self.processes["predictor"] = mp.Process(target=self.start_predictor, args=(date,))
		for proc_name, process in self.processes.items():
			process.start()

	def start_sensors(self, date):
		"""
		#TODO:
		- start one thread for each sensor
		- In each thread do:
			- call set_day(day)
			- do
				- read the sensor
				- save the data
				- save stats (mean, min, max) of the data in a file named [sensor.name]-[day].npy
				- concat all stats together in a file named [day].npy

		:param date:
		:return:
		"""
		for logger in self.sensor_loggers:
			logger.set_date(date)
			self.logger_to_thread[logger] = Thread(target=logger.read_and_log, daemon=True)
			self.logger_to_thread[logger].start()

	def stop_day(self, date):
		self.done_date.append(date)
		self.stop_sensors()
		self.stop_predictor()

	def stop_sensors(self):
		for sensor, thread in self.logger_to_thread.items():
			thread.join()

	def stop_predictor(self):
		for proc_name, process in self.processes.items():
			process.join()

	def start_predictor(self, day):
		"""
		#TODO:
		- read and add the data of the previous day to the training set.
		- re-train the model.
		-

		:param day:
		:return:
		"""
		raise NotImplementedError()

	def log_sensor_data(self, sensor):
		pass

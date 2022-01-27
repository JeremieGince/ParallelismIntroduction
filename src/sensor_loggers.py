import os
from threading import Lock
import numpy as np
import pandas as pd
from .sensors.sensor import Sensor
from .sensors.thermometer import Thermometer


class SensorLogger:
	sensors_data_folder = "./data/sensors_data/"
	sensors_data_filename = "datalog.csv"

	@staticmethod
	def new(sensor: Sensor):
		if isinstance(sensor, Thermometer):
			return ThermometerLogger(sensor)

	def __init__(self, sensor: Sensor):
		self._sensor = sensor
		self._date = None
		self._lock = Lock()

		# counter
		self.count = 0

		# stats
		self.min = np.inf
		self.mean = 0
		self.max = -np.inf

	@staticmethod
	def get_data_filename():
		return f"{SensorLogger.sensors_data_folder}/{SensorLogger.sensors_data_filename}"

	@property
	def columns_names(self):
		raise NotImplementedError()

	def set_date(self, date):
		self._date = date
		self._sensor.set_date(date)

	def create_load_log_file(self):
		with self._lock:
			if os.path.exists(SensorLogger.get_data_filename()):
				df = pd.read_csv(SensorLogger.get_data_filename(), index_col=['date'])
			else:
				df = pd.DataFrame(columns=["date", *self.columns_names])

			for col in ["date", *self.columns_names]:
				if col not in df.columns:
					df.insert(len(df.columns), col, np.NaN)

			df['date'] = pd.to_datetime(df['date'])
			df.set_index('date', inplace=True)
			df.to_csv(SensorLogger.get_data_filename())

	def update_log_file(self):
		with self._lock:
			df = pd.read_csv(SensorLogger.get_data_filename(), index_col=['date'])
			df.loc[pd.to_datetime(self._date), self.columns_names] = [self.min, self.max, self.mean]
			df.to_csv(SensorLogger.get_data_filename())

	def read_and_log(self):
		"""
		TODO: read the value of the sensor as much as it can and every time read is called, save the current stats
		TODO: on the shared file .csv

		tips: use lock to make sure you don't overwrite over other thread (sensor).

		:return: None
		"""
		self.create_load_log_file()
		while True:
			val = self._sensor.read()
			self.min = min(self.min, val)
			self.max = max(self.max, val)
			self.mean = (self.count * self.mean + val) / (self.count + 1)
			self.count += 1
			self.update_log_file()


class ThermometerLogger(SensorLogger):
	@property
	def columns_names(self):
		return ["TempLowF", "TempHighF", "TempAvgF"]

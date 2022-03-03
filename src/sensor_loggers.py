import multiprocessing as mp
import os
from threading import Thread, Event
from typing import Union

import numpy as np
import pandas as pd

from .sensors.sensor import Sensor


class SensorLogger(Thread):
	sensors_data_folder = "./data/sensors_data/"
	sensors_data_filename = "datalog.csv"

	def __init__(self, sensor: Sensor, lock: Union[mp.RLock, mp.Lock]):
		super().__init__()
		self._sensor = sensor
		self._date = None
		self._stop_event = Event()
		self.lock = lock
		# counter
		self.count = 0

		# stats
		self.min = np.inf
		self.mean = 0
		self.max = -np.inf

	@staticmethod
	def get_data_filename():
		return f"{SensorLogger.sensors_data_folder}/{SensorLogger.sensors_data_filename}"

	def set_date(self, date):
		self._date = date
		self._sensor.set_date(date)

	def stop(self):
		self._stop_event.set()

	def create_load_log_file(self):
		with self.lock:
			if os.path.exists(SensorLogger.get_data_filename()):
				df = pd.read_csv(SensorLogger.get_data_filename(), index_col=['Date'])
			else:
				df = pd.DataFrame(columns=["Date", *self._sensor.columns_names])

			for col in ["Date", *self._sensor.columns_names]:
				if col not in df.columns:
					df.insert(len(df.columns), col, np.NaN)

			df['Date'] = pd.to_datetime(df['Date'])
			df.set_index('Date', inplace=True)
			df.to_csv(SensorLogger.get_data_filename())

	def update_log_file(self):
		with self.lock:
			df = pd.read_csv(SensorLogger.get_data_filename(), index_col=['Date'])
			date = str(pd.to_datetime(self._date).date())
			print(date)
			df.loc[date, self._sensor.columns_names] = [self.min, self.max, self.mean]
			df.to_csv(SensorLogger.get_data_filename())

	def run(self):
		"""
		TODO: read the value of the sensor as much as it can and every time read is called, save the current stats
		TODO: on the shared file .csv

		tips: use lock to make sure you don't overwrite over other thread (sensor).

		:return: None
		"""
		self.create_load_log_file()
		while not self._stop_event.is_set():
			val = self._sensor.read()
			self.min = min(self.min, val)
			self.max = max(self.max, val)
			self.mean = (self.count * self.mean + val) / (self.count + 1)
			self.count += 1
			self.update_log_file()
	
	def join(self, timeout=None):
		self._stop_event.set()
		super(SensorLogger, self).join(timeout)

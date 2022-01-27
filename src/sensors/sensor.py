import os
import numpy as np
import pandas as pd
from threading import Lock


class Sensor:
	sensors_data_folder = "./data/sensors_data/"

	def __init__(self, sensor_id: int, name: str):
		self.sensor_id = sensor_id
		self.name = name
		self._date = None

		os.makedirs(Sensor.sensors_data_folder, exist_ok=True)

		# counter
		self.count = 0

		# stats
		self.min = np.inf
		self.mean = 0
		self.max = -np.inf

		self._lock = Lock()

	@property
	def columns_names(self):
		raise NotImplementedError()

	@property
	def data_filename(self):
		return f"{Sensor.sensors_data_folder}/{self._date}.csv"

	def set_date(self, date):
		self._date = date

	def read(self):
		raise NotImplementedError()

	def read_and_log(self):
		"""
		TODO: read the value of the sensor as much as it can and every time read is called, save the current stats
		TODO: on the shared file .csv

		tips: use lock to make sure you don't overwrite over other thread (sensor).

		:return: None
		"""
		while True:
			val = self.read()
			self.min = min(self.min, val)
			self.max = max(self.max, val)
			self.mean = (self.count * self.mean + val) / (self.count + 1)
			self.count += 1

			with self._lock:
				if os.path.isfile(self.data_filename):
					df = pd.read_csv(self.data_filename)
				else:
					df = pd.DataFrame(columns=["date", *self.columns_names])

				df[df["date"] == self._date]["date", *self.columns_names] = [self._date, self.min, self.max, self.mean]  # TODO: check if valid
				df.to_csv(self.data_filename)


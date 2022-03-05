import time
from multiprocessing import Lock, RLock, Event, Process
from typing import Union

import pandas as pd

from src.sensor_loggers import SensorLogger


class WeatherPredictor(Process):
	def __init__(self, lock: Union[RLock, Lock], done_dates: list = None):
		super().__init__()
		self._done_dates = done_dates if done_dates is not None else []
		self._date = None
		self.lock = lock
		self._stop_event = Event()

	def stop(self):
		self._stop_event.set()

	def set_done_date(self, done_dates):
		self._done_dates = done_dates

	def set_date(self, date):
		if self._date is not None:
			self._done_dates.append(self._date)
		self._date = date

	def run(self):
		while not self._stop_event.is_set():
			with self.lock:
				df = pd.read_csv(SensorLogger.get_data_filename(), index_col=['Date'])
				print(df)
				time.sleep(1.0)


















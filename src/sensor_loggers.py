import multiprocessing as mp
import os
from threading import Event, Thread
from typing import Union

import numpy as np
import pandas as pd

from .sensors.sensor import Sensor


class SensorLogger(Thread):
	sensors_data_folder = "./data/sensors_data/"
	sensors_data_filename = "datalog.csv"

	def __init__(self, sensor: Sensor, lock: Union[mp.RLock, mp.Lock]):
		"""
		Instantiateur de la classe SensorLogger. Hérite de Thread pour que les objets créés soient eux-mêmes des
		threads en quelque sorte.
		:param sensor: Senseur que le SensorLogger courant contrôle.
		:param lock: Objet `Lock` de multiprocessing (puisqu'il se déplace de process en process) pour verrouiller
		l'accès aux ressources / code.
		"""
		super(SensorLogger, self).__init__()
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
		"""
		Méthode statique qui permet d'accéder au fichier où est stocké les informations obtenues par les senseurs.
		:return: Le chemin pour accéder au fichier de stockage.
		"""
		return f"{SensorLogger.sensors_data_folder}/{SensorLogger.sensors_data_filename}"

	def set_date(self, date):
		"""
		Méthode permettant de changer la date courante pour le senseur.
		:param date: Date courante.
		"""
		self._date = date
		self._sensor.set_date(date)

	def stop(self):
		self._stop_event.set()

	def create_load_log_file(self):
		"""
		TODO
		:return:
		"""
		with self.lock:
			if os.path.exists(SensorLogger.get_data_filename()):
				df = pd.read_csv(SensorLogger.get_data_filename())
			else:
				fill = [self._date] + [np.nan] * len(self._sensor.columns_names)
				df = pd.DataFrame([fill], columns=["Date", *self._sensor.columns_names])

			for col in self._sensor.columns_names:
				if col not in df.columns:
					df.insert(len(df.columns), col, np.NaN)
			df.to_csv(SensorLogger.get_data_filename(), index=False)

	def update_log_file(self):
		"""
		TODO
		Returns
		-------

		"""
		with self.lock:
			df = pd.read_csv(SensorLogger.get_data_filename(), index_col="Date")
			date = self._date
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

import multiprocessing as mp
import time
from typing import List, Union

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

from exercice.sensors.sensor import Sensor


class PlotProcess(mp.Process):
	"""
	TODO: Objet héritant de mp.Processus servant à afficher les données de SensorLogger.get_data_filename() en
			temps réel.

			Tips: Utilisez mp.Lock afin de s'assurer de ne pas corrompe le fichier en l'ouvrant/le manipulant en
			même temps qu'un autre processus.
	"""
	def __init__(
			self,
			sensors: List[Sensor],
			lock: Union[mp.Lock, mp.RLock],
			log_file: str,
			date: str,
			update_dt: float = 1.0
	):
		"""
		Constructeur de PlotProcess.

		:param sensors: Liste des senseurs.
		:param lock: La serrure utilisée par les autres processus.
		:param log_file: Le nom/path du fichier contenant les données des senseurs courants.
		:param date: La date courante.
		:param update_dt: Le temps entre deux mises à jour du graphique.
		"""
		super(PlotProcess, self).__init__()
		self._sensors = sensors
		self._lock = lock
		self._close_event = mp.Event()
		self._log_file = log_file
		self._date = date
		self.update_dt = update_dt
		self.sensor_to_ax = {}
		self.sensor_to_lines = {}
		self._dates = None

	def run(self):
		"""
		TODO:
		Crée le graphique.
		Lance la boucle de mises à jour du graphique.
		:return: None
		"""
		raise NotImplementedError()

	def join(self, *args, **kwargs):
		"""
		Set le close event.
		Join le processus courant.
		"""
		self._close_event.set()
		return super(PlotProcess, self).join(*args, **kwargs)


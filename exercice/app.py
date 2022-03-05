import multiprocessing as mp
import time
import typing

import pandas as pd

from .interface.plot_process import PlotProcess
from .sensor_loggers import SensorLogger
from .sensors.sensor import Sensor
from .sensors_process import SensorsProcess


class App:
	def __init__(self, sensors: typing.List[Sensor], seconds_per_day: int = 100_000):
		"""
		Initialisateur de la classe App, classe qui s'occuper de partir les processus, qui eux s'occupent de partir
		les threads.
		:param sensors: Liste de senseurs qu'on veut utiliser.
		:param seconds_per_day: Nombre de secondes pour (simuler) une journée.
		"""
		self.sensors = sensors
		self._lock = mp.RLock()
		self.seconds_per_day = seconds_per_day
		self.done_date = list()
		self.sensors_process = None
		self.plot_process = None

	def run(self, n_day: typing.Union[int, str] = 'all'):
		"""
		Méthode permettant de simuler plusieurs journées. Appelle à l'interne `run_single_day`.
		:param n_day: Entier ou "all" (pour toutes les journées disponibles).
		:return: Rien
		"""
		with self._lock:
			dates = pd.read_csv(Sensor.rawData, index_col="Date").index.to_numpy()
		if n_day == 'all':
			n_day = len(dates)
		for date in dates[:n_day]:
			self.run_single_day(date)

	def run_single_day(self, date: str):
		"""
		Méthode permettant de simuler une seule journée. Démarre la journée, attend le temps de simuler la journée,
		puis termine la journée.
		:param date: date de la journée à simuler en format "AAAA-MM-JJ".
		:return:Rien.
		"""
		print(f"Start day - {date}")
		self.start_day(date)
		time.sleep(self.seconds_per_day)
		print(f"Stop day - {date}")
		self.stop_day(date)

	def start_day(self, date: str):
		"""
		TODO:
		Méthode permettant de démarrer la journée. On doit premièrement créer le processus de senseurs, puis celui
		qui permet l'affichage en temps réel.
		:param date: Date de la journée courante en format "AAAA-MM-JJ".
		:return: Rien
		"""
		raise NotImplementedError()

	def stop_day(self, date: str):
		"""
		Méthode permettant d'arrêter les processus démarrés en début de journée.
		:param date: Date de la journée à simuler en format "AAAA-MM-JJ".
		:return: Rien
		"""
		self.done_date.append(date)
		self.stop_processes()

	def stop_processes(self):
		"""
		TODO:
		Méthode permettant d'arrêter le processus gérant les threads, ainsi que celui gérant l'affichage en temps réel.
		On doit les joindre, les tuer et les fermer.
		:return: Rien
		"""
		raise NotImplementedError()

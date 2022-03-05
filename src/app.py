import multiprocessing as mp
import time
import typing

from .sensors.sensor import Sensor
from src.weather_predictor.weather_predictor import WeatherPredictor
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

	def run(self, n_day='all'):
		raise NotImplementedError()

	def run_single_day(self, date):
		"""
		Méthode permettant de simuler une seule journée. Démarre la journée, attend le temps de simuler la journée,
		puis termine la journée.
		:param date: date de la journée à simuler.
		:return:Rien.
		"""
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
		self.sensors_process = SensorsProcess(self.sensors, self._lock, date)
		self.sensors_process.start()

	def stop_day(self, date):
		"""
		Méthode permettant d'arrêter le processus gérant les threads (i.e. senseurs).
		:param date: Date de la journée à simuler.
		:return: Rien
		"""
		self.done_date.append(date)
		self.stop_processes()

	def stop_processes(self):
		"""
		Méthode permettant d'arrêter le prcessus gérant les threads.
		:return: Rien
		"""
		self.sensors_process.join()
		self.sensors_process.kill()
		self.sensors_process.close()


import multiprocessing as mp
import os
from threading import Event, Thread
import typing

import numpy as np
import pandas as pd

from .sensors.sensor import Sensor


class SensorLogger(Thread):
	sensors_data_folder = "./data/sensors_data/"
	sensors_data_filename = "datalog.csv"

	def __init__(self, sensor: Sensor, lock: typing.Union[mp.RLock, mp.Lock]):
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
		:param date: Date courante, dans le format "AAAA-MM-JJ"
		"""
		self._date = date
		self._sensor.set_date(date)

	def stop(self):
		"""
		Méthode permettant d'arrêter le Thread courant à l'aide d'un Event
		"""
		self._stop_event.set()

	def create_load_log_file(self):
		"""
		TODO
		Méthode permettant de créer le fichier de log s'il n'existe pas. S'il existe, on ajoute les colonnes dont
		on a besoin, remplies de NaN. S'il n'existe pas on se crée un DataFrame, on le remplit avec le nom des colonnes
		du senseur utilisé courant, et on met des NaN.
		TIP: Utiliser le lock de l'objet courant!
		:return: Rien
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
		Méthode permettant de mettre à jour le fichier de log. On lit le fichier, on accède à la ligne de la date
		courante et on met les données lues dans les bonnes colonnes.
		TIP: Utiliser le lock de l'objet courant!
		:return: Rien
		"""
		with self.lock:
			df = pd.read_csv(SensorLogger.get_data_filename(), index_col="Date")
			date = self._date
			df.loc[date, self._sensor.columns_names] = [self.min, self.max, self.mean]
			df.to_csv(SensorLogger.get_data_filename())

	def run(self):
		"""
		TODO
		Méthode fondamentale qui permet au Thread courant de fonctionner. Override `run` de threading.Thread.
		On doit lire le senseur attaché à l'objet courant, mettre à jour le minimum, le maximum et la moyenne observée
		dans la journée courante. Mettre à jour le count aussi (utile pour calculer la nouvelle moyenne). BIEN SûR:
		METTRE À JOUR LE LOG!!!!!
		TIP: Il faut une boucle tant qu'on n'arrête pas le Thread courant!
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
		"""
		Méthode permettant de fermer et joindre le Thread courant
		:param timeout: Temps avant de fermer automatiquement (en secondes). Défaut à `None`, pas de timeout.
		:return: Rien.
		"""
		self._stop_event.set()
		super(SensorLogger, self).join(timeout)

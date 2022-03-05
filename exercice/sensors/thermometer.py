import time

import pandas as pd
from scipy.stats import truncnorm

from .sensor import Sensor


class Thermometer(Sensor):
	def __init__(self, sensor_id: int, name="thermometer", units='Temperature [${}^\circ F$]'):
		"""
		Constructeur de la classe Thermometer. Un objet permettant de simuler un senseur de température.
		:param sensor_id: l'identifiant du senseur.
		:param name: Le nom du senseur. Défaut: "thermometer"
		:param units: Les unités des mesures pour l'affichage. Défaut: Temperature [${}^\circ F$]'
		"""
		super(Thermometer, self).__init__(sensor_id, name=name, units=units)
		self.acquisition_time = 0.1

	@property
	def columns_names(self):
		"""
		Propriété permettant d'accéder au nom des colonnes qui sont modifiées
		:return: Une liste de noms des colonnes
		"""
		return ["TempLowF", "TempHighF", "TempAvgF"]

	def read(self):
		"""
		Méthode simulant une lecture du senseur courant.
		:return: Une valeur aléatoire.
		"""
		time.sleep(self.acquisition_time)
		cols = self.columns_names
		data = pd.read_csv(Sensor.rawData, index_col="Date")
		low, high, avg = data.loc[self._date, cols]
		scale = max(high - avg, avg - low)
		a, b = (low - avg) / scale, (high - avg) / scale
		val = truncnorm.rvs(a, b, loc=avg, size=1, scale=scale).item()
		return val

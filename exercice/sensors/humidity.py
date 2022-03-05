import time

import pandas as pd
from scipy.stats import truncnorm

from .sensor import Sensor


class HumiditySensor(Sensor):
	def __init__(self, sensor_id: int, name: str = "humiditySensor", units: str = 'Humidity [%]'):
		"""
		Constructeur de HumiditySensor. Objet simulant un senseur d'humidité.
		:param sensor_id: L'identifiant du senseur courant.
		:param name: Le nom du senseur courant. Défaut: "humiditySensor".
		:param units: Les unités de mesures du senseur pour l'affichage. Défaut: 'Humidity [%]'.
		"""
		super(HumiditySensor, self).__init__(sensor_id, name, units=units)
		self.acquisition_time = 0.1

	@property
	def columns_names(self):
		"""
		Propriété permettant d'accéder au nom des colonnes qui sont modifiées
		:return: Une liste de noms des colonnes
		"""
		return ["HumidityLowPercent", "HumidityHighPercent", "HumidityAvgPercent"]

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

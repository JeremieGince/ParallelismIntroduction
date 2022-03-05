import pandas as pd
from scipy.stats import truncnorm
import time

from .sensor import Sensor


class DewPointSensor(Sensor):
	def __init__(self, sensor_id: int, name: str = "dewPointSensor", units='Temperature [${}^\circ F$]'):
		"""
		Instanciateur de la classe DewPointSensor, une classe créant des objets simulant des capteurs de point de rosée.
		:param sensor_id: id du senseur courant. N'a pas vraiment d'importance.
		:param name: Nom du senseur courant. Défaut à "dewPointSensor".
		:param units: Unités du senseur courant. Défaut à "Temperature [${}^\circ F$]", soit des degrés F.
		"""
		super(DewPointSensor, self).__init__(sensor_id, name, units=units)
		self.acquisition_time = 0.1

	@property
	def columns_names(self):
		"""
		Propriété permettant d'accéder au nom des colonnes qui sont modifiées dans le log par le SensorLogger qui
		s'occupe du senseur courant.
		:return: le nom des colonnes qui sont modifiées par le SensorLogger qui s'occuper du senseur courant.
		Dans le cas présent, c'est "DewPointLowF", "DewPointHighF", "DewPointAvgF".
		"""
		return ["DewPointLowF", "DewPointHighF", "DewPointAvgF"]

	def read(self):
		"""
		Méthode simulant la lecture du capteur courant. On dort un certain temps pour simuler l'acquisition.
		:return: la valeur du senseur courant
		"""
		time.sleep(self.acquisition_time)
		cols = self.columns_names
		data = pd.read_csv(Sensor.rawData, index_col="Date")
		low, high, avg = data.loc[self._date, cols]
		scale = max(high - avg, avg - low)
		a, b = (low - avg) / scale, (high - avg) / scale
		val = truncnorm.rvs(a, b, loc=avg, size=1, scale=scale).item()
		return val

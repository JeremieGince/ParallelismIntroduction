class Sensor:
	rawData = "./data/archive/austin_weather.csv"

	def __init__(self, sensor_id: int, name: str, units: str = '-'):
		"""
		Instantiateur de la classe Sensor, classe représentant un senseur virtuel. Sert à simuler des capteurs divers.
		Pour simuler un senseur particulier, simplement hériter de cette classe et override les méthodes
		qui ne sont pas implémentées
		:param sensor_id: entier représentant l'id du senseur courant. N'a pas vraiment de rôle à jouer, simplement
		pour le plaisir ;)
		:param name: nom du senseur courant. Permet de les démystifier entre eux par leur noms.
		:param units: Unités de mesure du senseur courant. Par défaut, unités arbitraires "-".
		"""
		self.sensor_id = sensor_id
		self.name = name
		self.units = units
		self._date = None

	@property
	def columns_names(self):
		"""
		Propriété qui permet d'obtenir le nom des colonnes du logger qui seront modifiées par le senseur courant.
		Ici, il n'est pas implémenté, à faire dans les classes qui hérite de Sensor.
		:return: Une erreur de non implémentation!
		"""
		raise NotImplementedError()

	def set_date(self, date: str):
		"""
		Méthode permettant de changer la date courante du senseur courant.
		:param date: Date courante en format "AAAA-MM-JJ".
		:return: Rien
		"""
		self._date = date

	def read(self):
		"""
		Méthode simulant une lecture du senseur courant.
		:return: Une erreur de non implémentation!
		"""
		raise NotImplementedError()

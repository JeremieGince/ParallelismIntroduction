import multiprocessing as mp
import typing
from .sensor_loggers import SensorLogger, Sensor


class SensorsProcess(mp.Process):
	def __init__(self, sensors: typing.List[Sensor], lock: typing.Union[mp.RLock, mp.Lock], date: str):
		"""
		Initialisateur de la classe SensorProcess.
		:param sensors: Liste de senseurs à considérer. Pour rappel, un senseur est un objet de type `Sensor` (ou dérivé
		de cette classe).
		:param lock: Objet `multiprocessing.Lock` ou `RLock` qui sert à protéger les ressources ouvertes, lues et
		modifiées.
		:param date: Date courante (en format "AAAA-MM-JJ")
		"""
		super(SensorsProcess, self).__init__()
		self.sensors = sensors
		self.lock = lock
		self.date = date
		self.exit_event = mp.Event()

	def run(self):
		"""
		TODO
		Méthode fondamentale pour que le processus courant fonctionne tant que la journée n'est pas finie.
		On doit bien sûr partir tous les Threads associés aux senseurs utilisés (i.e. partir des `SensorLogger`).
		On doit attendre que le la journée finisse. En fait, le processus courant ne fait pas grand chose
		(pas de boucle), car il ne termine pas tant que les threads internes ont finis ou on le termine manuellement.
		Lorsque la journée est finie, on ferme les threads courant
		:return: Rien
		"""
		sensor_loggers = [SensorLogger(sensor, self.lock) for sensor in self.sensors]
		for logger in sensor_loggers:
			logger.set_date(self.date)
			logger.start()
		self.exit_event.wait()  # Sert à attendre que le flag is_set() soit True
		for logger in sensor_loggers:
			logger.join()

	def join(self, timeout=None):
		"""
		Méthode permettant de joindre le processus courant, qui une fois joint, va fermer les threads internes.
		:param timeout: Temps avant de joindre le processus courant (en secondes). Défaut à `None`.
		:return: Rien
		"""
		self.exit_event.set()
		super(SensorsProcess, self).join(timeout)

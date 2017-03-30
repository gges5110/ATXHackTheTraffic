from database_setup import User, TravelSensor, Summary, db_session
import pickle
from create_map import Map

class Corridor(Map):
	READER_IDs = []
	ADJ_INTERSECTIONS = {}

	def get_map_from_database(self):
		travelSensors = db_session.query(TravelSensor).filter(TravelSensor.READER_ID.contains('lamar')).order_by(TravelSensor.LATITUDE.desc())
		self.READER_IDs = [x.READER_ID for x in travelSensors]
		for sensor in self.READER_IDs:
			print sensor

def get_map_from_file():
	return pickle.load('map.dump')


if __name__ == '__main__':
	m = Corridor()
	m.get_map_from_database()
	# m.create_corridor()

	output = open('map.dump', 'wb')
	pickle.dump(m, output)
	output.close()

from database_setup import Base, User, TravelSensor, Summary, db_session
import pickle

class Map:
	READER_IDs = []
	ADJ_INTERSECTIONS = {}

	def get_map_from_database(self):
		travelSensors = db_session.query(TravelSensor).all()
		self.READER_IDs = [x.READER_ID for x in travelSensors]
		for sensor in self.READER_IDs:
			self.ADJ_INTERSECTIONS[sensor] = db_session.query(Summary.DESTINATION).filter(Summary.ORIGIN==sensor).distinct(Summary.DESTINATION).all()
			print sensor
			print self.ADJ_INTERSECTIONS[sensor]

def get_map_from_file():
	return pickle.load('map.dump')


if __name__ == '__main__':
	m = Map()
	m.get_map_from_database()

	output = open('map.dump', 'wb')
	pickle.dump(m, output)
	output.close()


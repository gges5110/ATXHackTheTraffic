from database_setup import TravelSensor, Summary
from database_init import db_session
import cPickle as pickle

class Map:
	READER_IDs = []
	ADJ_INTERSECTIONS = {}

	def get_map_from_database(self):
		travelSensors = db_session.query(TravelSensor).all()
		self.READER_IDs = [x.READER_ID for x in travelSensors]
		for sensor in self.READER_IDs:
			adjs = db_session.query(Summary.Destination).filter(Summary.Origin==sensor).distinct(Summary.Destination).all()
			self.ADJ_INTERSECTIONS[sensor] = [adj[0] for adj in adjs]
			#print sensor
			#print self.ADJ_INTERSECTIONS[sensor]

	def get_map_from_file(self):
		ADJ_INTERSECTIONS = pickle.load(open('map.dump','rb'))
		self.ADJ_INTERSECTIONS = ADJ_INTERSECTIONS

	def create_map_cache(self):
		self.get_map_from_database()
		output = open('map.dump', 'wb')
		pickle.dump(m.ADJ_INTERSECTIONS, output)
		output.close()

if __name__ == '__main__':
	m = Map()
	# m.get_map_from_database()
	m.get_map_from_file()
	print m.ADJ_INTERSECTIONS
	# m.create_map_cache()

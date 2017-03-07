from database_setup import Base, User, TravelSensor, Summary, db_session
import pickle

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

def get_map_from_file():
	infile = open('map.dump','rb')
	return pickle.load(infile)


if __name__ == '__main__':
	m = Map()
	m.get_map_from_database()

	print m.ADJ_INTERSECTIONS

	output = open('map.dump', 'wb')
	pickle.dump(m, output)
	output.close()


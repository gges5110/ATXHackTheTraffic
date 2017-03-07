from database_setup import Base, User, TravelSensor, Summary, db_session
from create_map import Map, get_map_from_file

class Route:

	INFINITY = 1000000

	def __init__(self):
		travelSensors = db_session.query(TravelSensor).all()
		self.travelSensors = {x.READER_ID:(x.LATITUDE, x.LONGITUDE) for x in travelSensors}
		self.myMap = Map()
		self.myMap.get_map_from_database()

	def convertCoord(self, route):
		return [self.travelSensors[n] for n in route]

	def getAdjIntersections(self, node):
		if node not in self.myMap.ADJ_INTERSECTIONS:
			return []
		else:
			return self.myMap.ADJ_INTERSECTIONS[node]

	def getTravelTime(self, s, t, dtime, weekday):

		beg_day = 0
		end_day = 0

		if weekday in [0,1,2,3,4]:
			beg_day = 0
			end_day = 4
		else:
			beg_day = 5
			end_day = 6

		# first attempt
		summary = db_session.query(Summary).filter(
			Summary.Origin == s,
			Summary.Destination == t,
			Summary.Weekday == weekday,
			Summary.Time >= dtime/60,
			Summary.Time <= dtime/60+60,
			).order_by(Summary.Time).all()


		if len(summary) == 0:
			if dtime >= 23*3600:  # after 11pm, look at the next day
				summary = db_session.query(Summary).filter(
					Summary.Origin == s,
					Summary.Destination == t,
					Summary.Weekday == weekday+1
					).order_by(Summary.Time).all()

		if len(summary) == 0:
			summary = db_session.query(Summary).filter(
				Summary.Origin == s,
				Summary.Destination == t,
				Summary.Weekday >= beg_day,
				Summary.Weekday <= end_day,
				Summary.Time >= dtime/60,
				Summary.Time <= dtime/60+60,
				).order_by(Summary.Time).all()

		if len(summary) == 0:
			# report nothing
			#print "nothing"
			#print {'s':s, 't':t, 'dtime':dtime}
			return self.INFINITY

		looked_years = set()

		total = 0

		for ss in summary:
			if ss.Year not in looked_years:
				looked_years |= set([ss.Year])
				total += ss.Avg_Travel_Time

		#print {'s':s, 't':t, 'dtime':dtime, 'total':total, 'n': len(looked_years)}
		return total/len(looked_years)


	# weekday: Monday is 0
	def findRoute(self, s, t, dtime, weekday):
		# Priority queue
		Q = {s:dtime}
		# Dijkstra labels
		D = {s:dtime}
		P = {s:0}
		visited = set()

		while Q:
			u = min(Q, key=Q.get)
			Q.pop(u)
			visited |= set([u])

			if u == t:
				break;

			adjs = self.getAdjIntersections(u)
			for v in adjs:
				if v in visited:
					continue

				newt =  D[u] + self.getTravelTime(u,v,D[u],weekday)
				if (v not in D) or (newt < D[v]):
					Q[v] = newt
					D[v] = newt
					P[v] = u

		# backtracking
		route = [t]
		ptr = t
		while ptr != s:
			ptr = P[ptr]
			route.insert(0,ptr)

		return {'route': route, 'coord': self.convertCoord(route), 'time': D[t]}

	def findRoutes(self, s, t, dtime, weekday):
		result = [0]*5
		dayseconds = 60*60*24
		prev_weekday = weekday-1
		if prev_weekday < 0:
			prev_weekday = 6

		if (dtime > 15*60):
			result[0] = self.findRoute(s, t, dtime-15*60, weekday)
		else:
			result[0] = self.findRoute(s, t, dtime-15*60+dayseconds, prev_weekday)
		for i in range(0,4):
			dtime = dtime + 15*60
			if dtime > dayseconds:
				dtime = dtime - dayseconds
				weekday = (weekday + 1) % 7

			result[i] = self.findRoute(s, t, dtime, weekday)

		return result

time_prediction = Route()


if __name__ == '__main__':

	R = Route()
	#print R.findRoute(0,3,0,0)
	print "here"
	dtime = 16*60*60+30*60
	results= R.findRoutes('lamar_12th', 'lamar_barton_springs', dtime, 0)
	print results
	#print [result['time'] for result in results]
	#print R.convertCoord(result['route'])

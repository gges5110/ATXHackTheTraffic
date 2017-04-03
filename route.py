from database_setup import Base, TravelSensor, Summary
from database_init import db_session, engine
from create_map import Map
import sys
from Queue import PriorityQueue
from datetime import datetime

class Route:

	INFINITY = 1000000

	def __init__(self):
		travelSensors = db_session.query(TravelSensor).all()
		self.travelSensors = {x.READER_ID:(x.LATITUDE, x.LONGITUDE) for x in travelSensors}
		self.myMap = Map()
		self.myMap.get_map_from_file()

	def convertCoord(self, route):
		return [self.travelSensors[n] for n in route]

	def getAdjIntersections(self, node):
		if node not in self.myMap.ADJ_INTERSECTIONS:
			return []
		else:
			return self.myMap.ADJ_INTERSECTIONS[node]

	def getTravelTime(self, s, t, dtime, weekday):
		# first attempt
		summary = db_session.query(Summary.Year, Summary.Avg_Travel_Time).filter(
			Summary.Origin == s,
			Summary.Destination == t,
			Summary.Weekday == weekday,
			Summary.Time >= dtime/60,
			Summary.Time <= dtime/60+60,
			).order_by(Summary.Time).all()

		if len(summary) == 0:
			if dtime >= 23*3600:  # after 11pm, look at the next day
				summary = db_session.query(Summary.Year, Summary.Avg_Travel_Time).filter(
					Summary.Origin == s,
					Summary.Destination == t,
					Summary.Weekday == weekday+1
					).order_by(Summary.Time).all()

		if len(summary) == 0:
			beg_day = 0
			end_day = 0

			if weekday in [0,1,2,3,4]:
				beg_day = 0
				end_day = 4
			else:
				beg_day = 5
				end_day = 6

			summary = db_session.query(Summary.Year, Summary.Avg_Travel_Time).filter(
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
				looked_years.add(ss.Year)
				total += ss.Avg_Travel_Time

		#print {'s':s, 't':t, 'dtime':dtime, 'total':total, 'n': len(looked_years)}
		return total/len(looked_years)


	# weekday: Monday is 0
	def findRoute(self, s, t, dtime, weekday):
		travelTime = {}

		# Priority queue
		Q = {s:dtime}
		# Dijkstra labels
		D = {s:dtime}
		P = {s:0}
		visited = set()
		print "find route!"
		sys.stdout.flush()
		while Q:
			u = min(Q, key=Q.get)
			Q.pop(u)
			visited.add(u)

			if u == t:
				break;

			adjs = self.getAdjIntersections(u)
			for v in adjs:
				if v in visited:
					continue

				if (u,v,D[u],weekday) not in travelTime:
					travelTime[(u,v,D[u],weekday)] = self.getTravelTime(u,v,D[u],weekday)

				newt =  D[u] + travelTime[(u,v,D[u],weekday)]
				if (v not in D) or (newt < D[v]):
					Q[v] = newt
					D[v] = newt
					P[v] = u

		# backtracking
		route = [t]
		ptr = t
		while ptr != s and ptr in P:
			ptr = P[ptr]
			route.insert(0,ptr)

		if t in D:
			return {'route': route, 'coord': self.convertCoord(route), 'time': D[t]}
		else:
			return {'route': route, 'coord': self.convertCoord(route), 'time': -1}

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
	start_time = datetime.now()
	R = Route()
	dtime = 16*60*60+30*60
	# results= R.findRoutes('2nd_san_jacinto', '5th_campbell', dtime, 0)
	results = R.findRoutes('congress_oltorf', 'congress_11th', dtime, 0)
	print results
	end_time = datetime.now()
	total_time = end_time - start_time
	print "Start time:", str(start_time)
	print "End time:", str(end_time)
	print "Total time:", total_time.microseconds, "(us)"
	#print [result['time'] for result in results]
	#print R.convertCoord(result['route'])

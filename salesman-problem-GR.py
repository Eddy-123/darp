#solve traveling salesman problem using genetic algorithm
import math,random,time
import matplotlib.pyplot as plt

#Read coordinate file
filename = 'cities.txt' 
city_num = [] #City number
city_location = [] #City coordinates
with open(filename, 'r') as f:
    datas = f.readlines()[:]
for data in datas:
    data = data.split()
    city_num.append(int(data[0]))
    x = float(data[1])
    y = float(data[2])
    city_location.append((x,y))#City coordinates

def generate_indiced_path(cities, selected_indice):
	'''
		generate_path build the route to use
		greedy approach: search for the nearest city from the origin
		random approach: pick a city randomly to build the initial_path
		tabu search approach: invalid for the actual phase
		new approach: selection based on the position order
			hypothesis of new approach: the best parameters might depend on the order/position,
				that is more logical than random selction
			future work: the selection position might be determined by a math function that describes the best selection strategy
	'''
	path = []
	remain_cities = cities[:]
	curent_indice = 0
	
	while (len(remain_cities) > 0):
		curent_indice = curent_indice + selected_indice
		curent_indice = curent_indice % len(remain_cities)
		path.append(remain_cities[curent_indice])
		remain_cities.remove(remain_cities[curent_indice])
	return path

def initial_path(cities, selected_indice):
	initial_path = generate_indiced_path(cities, selected_indice)
	draw_path(initial_path, city_location)
	return initial_path

#Step: generate population using generate_indiced_path
def generate_population(cities, population_length):
	population = []
	for i in range(population_length):
		population.append(generate_indiced_path(cities, i))
	return population

#Step: crossover, one point and two points

def single_point_crossover(first_parent, second_parent, cross_point):
	first_part = first_parent[0:cross_point]
	second_part = [x for x in second_parent if x not in first_part]
	first_child = first_part + second_part
	
	first_part = second_parent[0:cross_point]
	second_part = [x for x in first_parent if x not in first_part]
	return first_child, second_child

def two_points_crossover(first_parent, second_parent, first_cross_point, second_cross_point):
	second_cross_point = ( second_cross_point +1 ) % len(first_parent)
	first_child = first_parent.copy()
	remain_indices = [x for x in range(len(first_parent)) if x not in range(first_cross_point, second_cross_point)]
	j = 0
	for i in remain_indices:
		while second_parent[j] in first_child[first_cross_point:second_cross_point]:
			j = j + 1
		first_child[i] = second_parent[j]
		j = j + 1
	#print("first child ", first_child)
	
	second_child = second_parent.copy()
	remain_indices = [x for x in range(len(second_parent)) if x not in range(first_cross_point, second_cross_point)]
	j = 0
	for i in remain_indices:
		while first_parent[j] in second_child[first_cross_point:second_cross_point]:
			j = j + 1
		second_child[i] = first_parent[j]
		j = j + 1

	return first_child, second_child

def draw_path(path, city_coordinates):
	x, y = [], []
	for i in path:
		coordinate = city_coordinates[i]
		x.append(coordinate[0])
		y.append(coordinate[1])
	x.append(x[0])
	y.append(y[0])
	
	plt.plot (x, 'r-', color='#4169E1', alpha = 0.8, linewidth = 0.8)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()

print("initial path ", initial_path(city_num, 4))

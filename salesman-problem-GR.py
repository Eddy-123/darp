#Solve traveling salesman problem using genetic algorithm
import math,random,time
import matplotlib.pyplot as plt

#Global variables
tabu_limit = 50

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

#Import distance matrix
def dist(file):
    X=[]
    matdis=[]
    with open(file,'r') as dis:
        datas=dis.readlines()[:]
    for data in datas:
        X=[]
        data=data.split()
        for i in range(26):
            x=float(data[i])
            X.append(x)
        matdis.append(X)
    return matdis


#calcuate the total distance of the path
#=============================================================================================================================
def fitness(path, distance_matrix):
	fit = 0.0
	for i in range(len(path) - 1):
		fit = fit + distance_matrix[i][i + 1]
	return fit


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


#Select best parents from the population
#=============================================================================================================================
def tabu_best_parents(population, distances, tabu_limit):
	tabu_list = population
	tabu_value_list = []
	best_path = []
	best_value = float('inf')
	for i in range(len(population)):
		new_path = population[i].copy()
		new_value = fitness(new_path, distances)
		if new_value < best_value:
			tabu_list.append(new_path)
			tabu_value_list.append(new_value)
			
			best_path = new_path
			best_value = new_value
			
			if len(tabu_list) >= tabu_limit:
				tabu_list.remove(tabu_list[0])
				tabu_value_list.remove(tabu_value_list[0])
				
	return tabu_list


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


#mutation function take a part of the path and flip it
#=============================================================================================================================
def mutation_revert(path):
    x = random.randint(0,cities_max)
    y = random.randint(0,cities_max)
    if x >= y :
        x, y = y, x

    mut=path.copy()
    j = x+((y-x)%2)
    for i in range(x, j+1):
        mut[i], mut[y - i] = mut[y - i], mut[i]
    return mut


def mutation_invert(path):
	x = random.randint(0,len(path) - 1)
	y = random.randint(0,len(path) - 1)
	mut = path
	if x >= y :
		x, y = y, x
	
	mut[x], mut[y] = mut[y], mut[x]
	return mut

def get_best_path(population, distance_matrix):
	best_path = []
	best_value = float('inf')
	for i in range(len(population)):
		new_path = population[i]
		new_value = fitness(population[i], distance_matrix)
		if new_value < best_value:
			best_path = new_path
			best_value = new_value
	return best_path, best_value

def draw_path(path, city_coordinates):
	x, y = [], []
	for i in range(len(path)):
		coordinate = path[i]
		x = x + [coordinate[0]]
		y.append(coordinate[1])
	x.append(x[0])
	y.append(y[0])
	
	plt.plot(x, y)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()

def fig():
    time_start = time.time()
    N = 1000 #Evolution times
    satisfactory_solution,mile_cost,record = main(N)
    time_end = time.time()
    time_cost = time_end - time_start
    print('time cost:',time_cost)
    print("Optimize mileage cost: %d" %(int(mile_cost)))
    print("Optimization Path:\n",satisfactory_solution)
    #Drawing a route map
    X = []
    Y = []
    for i in satisfactory_solution:
        x = city_location[i-1][0]
        y = city_location[i-1][1]
        X.append(x)
        Y.append(y)
    plt.plot(X,Y,'-o')
    plt.title("satisfactory solution of TS:%d"%(int(mile_cost)))
    plt.show()
    #Draw iterative process diagram
    A = [i for i in range(N+1)]#Abscissa
    B = record[:] #Y-axis
    plt.xlim(0,N)
    plt.xlabel('Number of evolution',fontproperties="SimSun")
    plt.ylabel('Path mileage',fontproperties="SimSun")
    plt.title("solution of GA changed with evolution")
    plt.plot(A,B,'-')
    plt.show()
    return mile_cost,time_cost
#Parameters
population_size = 100
iter_generation = 1000
cross_point = 2
tabu_limit = 50

#cities
cities = city_location

#distance matrix
distances = dist('distance.txt')

#initial population
population = generate_population(cities, population_size)

i = 0
best_path_list = list()

#print("test = ok")

while i < iter_generation:
    #chose the best N paren
	parents = tabu_best_parents(population, distances, tabu_limit)
	
    #the crossover
	target_count = population_size - len(parents)
	children = []
	while len(children) < target_count:
		#stop: parent1 = parents()
		#print(parents)
		#print(len(parents))
		child1 , child2 = single_point_crossover(parent1,parent2,cross_point)
	
	#mutation
	for j in range (len(parents)):
		parents[j] =  mutation_invert(parents[j])
	for j in range (len(children)):
		if random.random()<= 0.3:
			children[j] =  mutation(children[j])
	
	best_path = get_best_path(population, distances)
	best_path_list = best_path_list + [best_path]
	print("best path list = ", len(best_path_list))
	population = parents + children
	
	i = i + 1

print("Start drawing")

print("result ", best_path_list[-1])

#draw_path(best_path_list[0][0], cities)
#draw_path(best_path_list[-1][0], cities)

#fig()
#print("best path at the begining : ", fitness(best_path_list[0], distances))
#print("best path at the end : ", fitness(best_path_list[-1], distances))

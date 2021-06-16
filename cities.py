import math,random,time
import os
#Read coordinate file
filename = 'cities.txt' 
city_num = [] #City number
city_locations = [[0,0,0]] #City coordinates
cities=[0]
city=[]
#create a list of random located cities
def cities_generate(file):
    if os.path.exists(file):
        os.remove(file)
    cities=[]
    with open(file, 'a') as the_file:
        the_file.write('{} {} {} {} {}\n'.format(0, 0, 0, 0, 0))
        for i in range(1, 26):

            x=int(random.random() * 200)
            y=int(random.random() * 200)
            th=random.randint(8, 18)
            tm=random.randint(0, 59)
            city=[i,x,y]
            cities.append(i)
            city_locations.append(city)
            the_file.write('{} {} {} {} {}\n'.format(i, x, y, th, tm))


print("The file was successfully created")
#=========================================================================
#create a file with distance matrix
def mat_dis(file):
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'a') as dis:
        for k in range(26):
            dis.write('{} '.format(k))
        dis.write('\n')
        for i in range(1,26):
            for j in range(26):
                if j == 0:
                    dis.write('{} '.format(i))
                else:
                    x=city_locations[i][1]-city_locations[j][1]
                    y=city_locations[i][2]-city_locations[j][2]
                    
                    dist = round(math.hypot(x, y),2)
                    dis.write('{} '.format(dist))
            dis.write('\n')

#==========================================================================
#import distance matrix and use it
def cities_list(file):
    X=[]
    cities=[]
    with open(file,'r') as f:
        datas=f.readlines()[:]
        for data in datas :
            X=[]
            data=data.split()
            X=data.copy()
            for i in range(5):
                X[i]=float(X[i])
            cities.append(X)
        return cities
            
        
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
cities_generate('cities.txt')
mat_dis('distance.txt')
print(dist('distance.txt'))





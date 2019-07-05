import json
import random



# 1 LOAD JSON FILE

#with open('../../../JSON/Cities.json') as data_file:
#    data = json.load(data_file)
#city_list = list(data['Cities'])


# 2 TAKE TOWN AND PERCENT OUT
#cities = ['London', 'Adelade','Paris','Moscow','Aukland','Barcelona','Budapest','Cardiff','Cincinnati','Copenhagen','Detroit','Dublin','Ho Chi Minh City','Hanoi','Lisbon','Los Angeles','Madrid','Manchester','Miami','New Delhi','Pittsburgh','Quito','Pune','Sapporo','Shanghai','Zhangjiakou','Wellington','Vladivostok']
try:
        
    cities = ['Adelade', 'Aukland']
    town1 = random.choice(cities)

    print town1

    path_json_file = "../../../git-data/JSON/"
    path_json_file += town1
    path_json_file += ".json"
    dataset_town1 = json.loads(open(path_json_file).read())

    percent = 20



    for city_percent in dataset_town1:
            print city_percent['Percentage']
            print city_percent['City_Name']  
            N = 10000
            N *= city_percent['Percentage']
            print N  
            percent = city_percent['Percentage']

    print percent


# 3 MULTIPLY N = NO. NODES BY PERCENTAGE



#4 LOOP LIST FOR ALL VALUES IN THE LIST 

# 5 PRINT OUT LIST OF THE RESULTS 


#print(json.dumps(city_list['Percentage']))
#i = 0
#city_values = city_list[:]

#while i < len(city_values):
#    print(city_values[:]["Percentage"])
#    i += 1




except IOError:
   print("File not found or path is incorrect")
finally:
   print("------------------")

import json
import string
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.stats import norm

def deleteMS( str ):
    b = "ms"
    for char in b:
        str = str.replace(char,"")
    return str

def deleteKM( str ):
    b = "km"
    for char in b:
        str = str.replace(char,"")
    return str

try:
    # ALL Cities
    Cities = json.loads(open('C:/Users/JosephKearney/Desktop/JSON/Cities.json').read())
    num = random.randint(0, 245)
    print('Random Town ->', Cities[num])
    # -London- Dataset
    LondonDatase = json.loads(open('C:/Users/JosephKearney/Desktop/JSON/London.json').read())
    # -Paris- Dataset
    ParisDataset = json.loads(open('C:/Users/JosephKearney/Desktop/JSON/Paris.json').read())
    # -Moscow- Dataset
    MoscowDataset = json.loads(open('C:/Users/JosephKearney/Desktop/JSON/Moscow.json').read())

    print("------------------")
    print('London to ->', LondonDatase[0]['City'],deleteKM(LondonDatase[0]['Distance']),deleteMS(LondonDatase[0]['Average']))
    print('Paris  to ->', ParisDataset[0]['City'],deleteKM(ParisDataset[0]['Distance']),deleteMS(ParisDataset[0]['Average']))
    print('Moscow to ->', MoscowDataset[0]['City'],deleteKM(MoscowDataset[0]['Distance']),deleteMS(MoscowDataset[0]['Average']))

except IOError:
    print("File not found or path is incorrect")
finally:
    print("------------------")


# plt.plot([1,2,1,4,2])
# plt.show()

# plt.plot([1,2,3,4,5], [1,4,9,16,5], 'ro')
# plt.axis([0, 6, 0, 20])
# plt.show()



# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title('Histogram of IQ')
# plt.text(60, .025, r'$\mu=100,\ \sigma=15$')


# ax = plt.subplots()
# plt.plot([100,220,300,400], [100,400,90,160], 'ro', linestyle='solid')
# # https://stackoverflow.com/questions/12043672/how-to-take-draw-an-average-line-for-a-scatter-a-plot-in-matplotlib
# plt.axis([0, 500, 0, 500])
# plt.show()

#----------------------------------------------------


# Plot between -10 and 10 with .001 steps.
#                  min  max  steps
# x_axis = np.arange(-10, 10, 0.05)
# #                                mean  mdev
# plt.plot(x_axis, norm.pdf(x_axis , 0 , 2) )
# plt.show()

#------------------------------------------------------

x_axis = np.arange(293, 294, 0.001)
plt.plot(x_axis, norm.pdf(x_axis , 293.6 , 0.1) )
plt.show()

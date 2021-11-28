import csv
import numpy as np
import matplotlib.pyplot as plt

def statepop2000():
    with open('2000StatePopulation.csv','r') as f:
        states = list(csv.reader(f))
    states = np.array(states[1:])
    statepops2000 = np.delete(states,2,1)
    return statepops2000

def plot2000():
    statepops2000 = statepop2000()
    x = statepops2000[:,1]
    y_strings = statepops2000[:,0]
    y = []
    for i in y_strings:
        y.append(float(i))
    fig = plt.figure()
    plt.bar(x,y, color = 'maroon')
    plt.xticks(x,rotation=90)
    plt.xlabel('States in the US', fontweight = 'bold', color = 'orange', fontsize = '8', horizontalalignment = 'center')
    plt.ylabel('Population(*10^7)')
    plt.subplots_adjust(bottom=0.4)
    plt.title('2000 Census Data')
    plt.savefig('2000Population.png')

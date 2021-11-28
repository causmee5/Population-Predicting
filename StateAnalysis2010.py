import csv
import numpy as np
import matplotlib.pyplot as plt

def statepop2010():
    with open('2010StatePopulation.csv','r') as f:
        states = list(csv.reader(f))
    states = np.array(states[1:])
    statepops2010 = np.delete(states,2,1)
    return statepops2010

def plot2010():
    statepops2010 = statepop2010()
    x = statepops2010[:,1]
    y_strings = statepops2010[:,0]
    y = []
    for i in y_strings:
        y.append(float(i))
    fig = plt.figure()
    plt.bar(x,y, color = 'maroon')
    plt.xticks(x,rotation=90)
    plt.xlabel('States in the US', fontweight = 'bold', color = 'orange', fontsize = '8', horizontalalignment = 'center')
    plt.ylabel('Population(*10^7)')
    plt.subplots_adjust(bottom=0.4)
    plt.title('2010 Census Data')
    plt.savefig('2010Population.png')

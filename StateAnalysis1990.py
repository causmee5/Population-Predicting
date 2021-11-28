import csv
import numpy as np
import matplotlib.pyplot as plt

def statepop1990():
    with open('1990StatePopulation.csv','r') as f:
        states = list(csv.reader(f))
    states = np.array(states[1:])
    statepops1990 = np.delete(states,2,1)
    return statepops1990

def plot1990():
    statepops1990 = statepop1990()
    x = statepops1990[:,1]
    y_strings = statepops1990[:,0]
    y = []
    for i in y_strings:
        y.append(float(i))
    fig = plt.figure()
    plt.bar(x,y, color = 'maroon')
    plt.xticks(x,rotation=90)
    plt.xlabel('States in the US', fontweight = 'bold', color = 'orange', fontsize = '8', horizontalalignment = 'center')
    plt.ylabel('Population(*10^7)')
    plt.subplots_adjust(bottom=0.4)
    plt.title('1990 Census Data')
    plt.savefig('1990Population.png')

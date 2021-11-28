import StateAnalysis1990
import StateAnalysis2000
import StateAnalysis2010
import csv
import numpy as np
import matplotlib.pyplot as plt

def comparestatepop():
    statepop1990 = StateAnalysis1990.statepop1990()
    statepop2000 = StateAnalysis2000.statepop2000()
    statepop2010 = StateAnalysis2010.statepop2010()
    pops1990 = [float(i) for i in statepop1990[:,0]]
    pops2000 = [float(i) for i in statepop2000[:,0]]
    pops2010 = [float(i) for i in statepop2010[:,0]]
    del pops2010[-1]
    changefrom1990to2000 = np.array(pops2000,dtype=float)-np.array(pops1990,dtype=float)
    #changefrom1990to2010 = np.array(pops2010,dtype=float)-np.array(pops1990,dtype=float)
    #changefrom2000to2010 = np.array(pops2010,dtype=float)-np.array(pops2000,dtype=float)
    predictionfor2010 = np.array(pops2010,dtype=float)+changefrom1990to2000
    return predictionfor2010

def comparisonplots():
    statepops1990 = StateAnalysis1990.statepop1990()
    states = statepops1990[:,1]
    predictionfor2010 = comparestatepop()
    plt.bar(states,predictionfor2010,align='edge')
    plt.xticks(states,rotation=90)
    plt.xlabel('States in the US', fontweight = 'bold', color = 'orange', fontsize = '8', horizontalalignment = 'center')
    plt.subplots_adjust(bottom=0.4)
    plt.title('Prediction of 2010 Census Data')
    plt.savefig('2010Prediction.png')

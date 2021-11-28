import StateAnalysis1990
import StateAnalysis2000
import StateAnalysis2010
import comparestatepop

def main():

    comparestatepop.comparisonplots()

    StateAnalysis1990.plot1990()
    StateAnalysis2000.plot2000()
    StateAnalysis2010.plot2010()

if __name__ == "__main__":
    main()

# trainingLoad
import subprocess
from pathlib import Path
from datetime import datetime
import os

class data:
    def __init__(self, file):
        self.file = file
        self.durations [100] = []
        self.distance [100] = []
        self.sleep [100] = []
        self.trainingLoad = 0

    def parseJsonFile(self):
        file = open(self.file, "r")
        f = file.readlines()
        topLine = f[0].split(",")
        for i in range (100):
            parser = f[len(f)-i].split(",")
            self.durations[i] = parser[17]
            self.distance[i] = parser[18]
            self.sleep[i] = parser[10] 

    def getTrainingLoad(self):
        # Scale of 0 - 1000
        # 0-250: Low risk/not training enough
        # 251-500: Low risk but training enough
        # 501-750: Higher risk but training enough
        # 751-1000: High risk

        # Based on sleep, mileage
        # Sleep has lower risk
        # Compare mileage for 7 days to a previous days
        # Bad if greater > 20%
        sum1 = 0
        sum2 = 0
        mileageFactor = 2.0
        sleepFactor = 1.0
        durationFactor = 1.5
        for i in range (len(self.distance)):
            for j in range (7):
                sum1 += self.distance[j+i]
                sum2 += self.distance[j+7+i]
            if (((sum1-sum2)/sum2) > .2):
                mileageFactor = 2.7
            sum1, sum2 = 0
            for j in range (7):
                sum1 += self.duration[j+i]
                sum2 += self.duration[j+7+i]
            if (((sum1-sum2)/sum2) > .2):
                durationFactor = 1.9
            sum1, sum2 = 0
            for j in range(7):
                sum1 += self.sleep[j+i]
            if ((sum1/7) < 8.0):
                sleepFactor = .7
            sum1 = 0
        
        recentMileage = 0
        recentDuration = 0
        recentSleep = 0
        for i in range(7):
            recentMileage += self.distance[i]
            recentDuration += self.duration[i]
            recentSleep += self.sleep[i]

        self.trainingLoad = (mileageFactor * recentMileage) + (durationFactor * recentDuration) - (recentSleep * sleepFactor)

        # Most Recent -> Least Recent



def main():
    # -u username -p password -c chromedriver path -d days -o output path
    username = ""
    password = ""
    date = datetime.now()
    dateStr = date.strftime('%Y-%m-%d')
    date2 = date - datetime.timedelta(days = 50)
    date2Str = date2.strftime('%Y-%m-%d')
    path = Path("chromedriver")
    output = os.path.dirname(os.path.realpath(__file__)) + dateStr + ".csv"
    subprocess.run(["pygce", "-u", username, "-p", password, "-c", path, "-d", date2Str, dateStr, "-o", output])
    # get file from subprocess 
    file = dateStr + ".csv"
    tl = data(file).getTrainingLoad
    print("Your training load is ", tl)

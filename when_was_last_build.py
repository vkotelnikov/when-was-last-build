import re
import os
from datetime import datetime, time
import time as tsleep

project = None
projectLastBuilt = None

def checkForBuild():
    fileDate = str(datetime.now().date())
    filename = os.getenv('CATALINA_HOME') + '\logs\catalina.{date}.log'.format(date=fileDate)
    checkResult = {}
    try:
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            for line in list(lines)[::-1]:
                if 'finished' in line:
                    global projectLastBuilt
                    projectLastBuilt = datetime.strptime(line[:20], '%d-%b-%Y %H:%M:%S')
                    pattern = re.compile(r"(?<=\\)(\w+)(?=\.war])")
                    match = pattern.search(line)
                    if match:
                        global project
                        project = match.group(0)
                        checkResult['checkTime'] = datetime.now()
                        checkResult['checkTimeStr'] = datetime.now().strftime('%H:%M:%S')
                        checkResult['buildTime'] = projectLastBuilt
                        checkResult['project'] = project
                    return checkResult
    except:
        return None


if __name__=='__main__':
    res=None
    while True:
        try:
            res = checkForBuild()
        except:
            print('No log file found')
            tsleep.sleep(10)
            continue
        clear = lambda: os.system('cls')  
        clear()
        if not res:
            print("There was no builds today")
        else:
            print("Checked at {0}".format(res['checkTime']))
            print("Last build was {0} at {1}".format(res['project'], res['buildTime']))
            print("Diff from now: {0}\n".format(res['checkTime'] - res['buildTime']))
        tsleep.sleep(10)


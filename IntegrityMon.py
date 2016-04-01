import hashlib
import time
import os

def getLog():
    num = str(len(os.listdir(directory)))
    logFile = open(directory+"\\"+num,"r")
    for line in logFile.read().split("\n")[:-1]:
        line = line.split("\t\t\t")
        currentHashes.update({line[0]:line[1]})
    logFile.close()

def generateLog():
    num = str(len(os.listdir(directory))+1)
    text = ""
    for key in currentHashes:
        text+="{}\t\t\t{}\n".format(key,currentHashes[key])
    logFile = open(directory+"\\"+num,"w")
    logFile.write(text)
    logFile.close()

def createDirectory(directory):
    try:
        os.mkdir(directory)
        return True
    except:
        return False

def removeIllegal(path):
    for item in '\/:*?"<>|.':
        path = path.replace(item,"_")
    return path

target = raw_input("Target Directory: ")    
directory = removeIllegal(target)
currentHashes = {}
if createDirectory(directory):
    for root,directories,files in os.walk(target):
        for item in files:
            tmpPath = root+"\\"+item
            currentHashes.update({tmpPath:hashlib.md5(open(tmpPath,"rb").read()).hexdigest()})
    generateLog()
else:
    getLog()

print "\nMonitoring Target Directory. . .\n"
while True:
    time.sleep(5)
    tmpHashes = {}
    new = []
    changed = []
    deleted = []
    for root,directories,files in os.walk(target):
        for item in files:
            tmpPath = root+"\\"+item
            tmpHashes.update({tmpPath:hashlib.md5(open(tmpPath,"rb").read()).hexdigest()})
    if currentHashes != tmpHashes:
        for key in currentHashes:
            if key not in tmpHashes:
                deleted.append(key)
            elif currentHashes[key] != tmpHashes[key]:
                changed.append(key)
        for key in tmpHashes:
            if key not in currentHashes:
                new.append(key)
        print "NEW FILES:"
        if new != []:
            for item in new:
                print "\t"+item
        else:
            print "\tNone"
        print "CHANGED FILES:"
        if changed != []:
            for item in changed:
                print "\t"+item
        else:
            print "\tNone"
        print "DELETED FILES:"
        if deleted != []:
            for item in deleted:
                print "\t"+item
        else:
            print "\tNone"
        print ""
        currentHashes = tmpHashes
        generateLog()

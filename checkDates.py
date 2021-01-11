import datetime
import json
from pathlib import Path
import re
import subprocess

verbose = False
folderPattern = re.compile("([\d]{4})-([\d]{2})")


def handleYears(base):    
    for year in range(2013, 2015):
        handleYear(base, str(year))


def handleYear(base, year):
    if verbose:
        print('Year:', year)

    path = Path(base, year)
    for monthFolder in path.iterdir():
        handleDir(monthFolder)


def handleDir(folder):
    path = Path(folder)
    folderName = path.parts[-1]

    print('Folder:', folder)

    match = folderPattern.fullmatch(folderName)
    if match is None:
        if verbose:
            print("Ignoring", folder)
        return

    folderYear = match.group(1)
    folderMonth = match.group(2)
    
    command = "exiftool {} -CreateDate -json".format(folder)
    output = subprocess.check_output(command, shell=True)
    list = json.loads(output)

    for entry in list:
        fileName = entry["SourceFile"]
        rawDate = entry["CreateDate"]

        date_time_obj = datetime.datetime.strptime(rawDate, '%Y:%m:%d %H:%M:%S')
        imageDate = date_time_obj.strftime("%Y-%m")

        imageYear = date_time_obj.year
        imageMonth = date_time_obj.month

        needToMove = imageDate != folderName
        if needToMove:
            print('File:', fileName, " - found", imageDate)
        else:
            if verbose:
                print('File:', fileName, " - ok")


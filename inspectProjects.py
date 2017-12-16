#!/usr/bin/env python3

import AllProjectsJava
import AllProjectsCPP
import optparse
import json

"""
inspectProjects.py.

"""

def buildAllProjects(jsonfile, weShouldPause=False, selectStudent=None, limit=0):
    """
    Creates an AllProjects object.
    """

    dictionary = json.loads(open(jsonfile).read())
    projects = {}

    if dictionary["Language"] == "Java":
        projects = AllProjectsJava.AllProjectsJava(dictionary["AllProjectsZipFile"],
                                           dictionary["FileToLaunch"],
                                           dictionary["FilesToInspect"],
                                           dictionary["ClassPath"],
                                           selectStudent,
                                           limit,
                                           weShouldPause)
    elif dictionary["Language"] == "CPP":
        projects = AllProjectsCPP.AllProjectsCPP(dictionary["AllProjectsZipFile"],
                                           dictionary["Folder"],
                                           dictionary["Tests"],
                                           selectStudent,
                                           limit,
                                           weShouldPause)
        
    return projects

def showSimpleJSON():
    print("""{
    "AllProjectsZipFile": "allProjects.zip",
    "Language": "Java",
    "FileToLaunch" : null,
    "Folder": "StudentProjects",
    "FilesToInspect": ["src/model/file1.java",
                       "src/model/file2.java",
                       "src/model/file3.java"],
    "ClassPath": null
}""")

if __name__=='__main__':
    desc = """Student Project Inspector"""
    p = optparse.OptionParser(usage="%prog [options] [file]", version="%prog 0.1", description=desc)

    p.add_option("-p", "--pause", action="store_true", dest="weShouldPause", help="Requires that the user hit 'enter' after every student record.", default=False)
    p.add_option("-j", "--json", action="store_true", dest="showJSON", help="Show a sample JSON configuration and quit.", default=False)
    p.add_option("-s", "--student", dest="selectStudent", help="Process files starting with this student's name", metavar="John")
    p.add_option("-f", "--file", dest="filename", help="JSON configuration file", metavar="FILE")
    p.add_option("-l", "--limit", dest="limit", help="Limit processing to N students (0 means unlimited)", metavar="5", default=0)
    options, arguments = p.parse_args()

    if options.filename is not None:
        projects = buildAllProjects(options.filename, options.weShouldPause, options.selectStudent, options.limit)

        projects.unzipProjects()
        projects.executeProjects()
    elif options.showJSON:
        showSimpleJSON()
    else:
        print("This program needs an JSON configuration file to work.")

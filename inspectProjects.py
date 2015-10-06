import AllProjects
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
    projects = AllProjects.AllProjects(dictionary["AllProjectsZipFile"],
                                       dictionary["FileToLaunch"],
                                       dictionary["FilesToInspect"],
                                       dictionary["ClassPath"],
                                       selectStudent,
                                       limit,
                                       weShouldPause)
    return projects

if __name__=='__main__':
    desc = """Student Project Inspector"""
    p = optparse.OptionParser(usage="%prog [options] [file]", version="%prog 0.1", description=desc)

    p.add_option("-p", "--pause", action="store_true", dest="weShouldPause", help="Requires that the user hit 'enter' after every student record.", default=False)
    p.add_option("-s", "--student", dest="selectStudent", help="Process files starting with this student's name", metavar="John")
    p.add_option("-f", "--file", dest="filename", help="JSON configuration file", metavar="FILE")
    p.add_option("-l", "--limit", dest="limit", help="Limit processing to N students (0 means unlimited)", metavar="FILE", default=0)
    options, arguments = p.parse_args()

    if options.filename is not None:
        projects = buildAllProjects(options.filename, options.weShouldPause, options.selectStudent, options.limit)
        projects.unzipProjects()
        projects.executeProjects()
    else:
        print("This program needs an JSON configuration file to work.")

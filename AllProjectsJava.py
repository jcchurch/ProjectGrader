import StudentProjectJava
import zipfile
import glob
import os

class AllProjectsJava:

    def __init__(self, sourceZip, mainClass=None, filesToInspect=[], classpath=None, selectStudent=None, limit=0, weShouldPause=False):
        """
        Creates the AllProjects object.

        @param sourceZip A string of a zipfile containing every student's
                         projects (which are zip files themselves).
        @param mainClass A string of the java class file containing 'main' which
                         Java should execute.
        @param filesToInpect A list of files which should be found in
                             the project that the students have contributed
                             and require inspection from the professor.
        @param limit         Limit our execution to this many students.
                             0 means all of them.
        @param selectStudent A string representing part of a student's name
                             which will be used to limit the execution of
                             'executeProjects' to just those containing this
                             name. If this variable is None, it is ignored.
        """

        self.sourceZip = sourceZip
        self.mainClass = mainClass
        self.filesToInspect = filesToInspect
        self.classpath = classpath 
        self.selectStudent = selectStudent
        self.limit = limit
        self.weShouldPause = weShouldPause 
        self.folder = "StudentProjects"

    def unzipProjects(self):
        """
        Unzips the giant moddle file of all student
        projects to a new directory.

        This first creates a new folder for the projects.
        If the folder already exists, we assume that
        the project has already been unzipped.

        @returns nothing
        """

        if os.path.isdir(self.folder) == False:
            os.mkdir(self.folder)

            zipObject = zipfile.ZipFile(self.sourceZip, 'r')
            zipObject.extractall(path=self.folder)
            print("Created and unziped all student projects.")

    def processStudentProject(self, thisZipFile):
        """
        Creates a StudentProject object and executes it.
        This method assumes that we are inside

        @param thisZipFile A zipfile representing a student's project
        @returns nothing
        """

        project = StudentProjectJava.StudentProjectJava(thisZipFile, self.mainClass, self.filesToInspect, self.classpath)
        project.start()

    def executeProjects(self):
        """
        Moves into the folder containing all student projects
        and one-buy-one calls 'processStudentProject' on each.

        If self.selectStudent is not None, only zipfiles containing
        a portion of a student's name identified by self.selectStudent
        will be processed.

        After all student projects have been processed, we move one
        level up out of the folder.
        """

        # Move in
        os.chdir(self.folder)

        studentZipFiles = glob.glob('*.zip') + glob.glob('*.tgz')
        studentZipFiles.sort()

        numberProcessed = 0
        processZipFiles = False

        if self.limit == 0:
            self.limit = len(studentZipFiles)

        if self.selectStudent is None:
            processZipFiles = True

        for thisZipFile in studentZipFiles:

            if numberProcessed < self.limit and (
                processZipFiles or
                self.selectStudent is None or
                self.selectStudent in thisZipFile
               ):
                self.processStudentProject(thisZipFile)
                processZipFiles = True
                numberProcessed += 1

                if self.weShouldPause:
                    input("Press enter to continue.")

        # Move up
        os.chdir("../")

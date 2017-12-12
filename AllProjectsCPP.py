import StudentProjectCPP
import zipfile
import glob
import os

class AllProjectsCPP:

    def __init__(self, sourceZip, tests=[], selectStudent=None, limit=0, weShouldPause=False):
        """
        Creates the AllProjects object.

        @param sourceZip A string of a zipfile containing every student's
                         projects (which are zip files themselves).
        """

        self.sourceZip = sourceZip
        self.tests = tests
        self.folder = "cppfiles"
        self.limit = limit
        self.selectStudent = selectStudent
        self.weShouldPause = weShouldPause

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

    def processStudentProject(self, filenames):
        """
        Creates a StudentProject object and executes it.
        This method assumes that we are inside

        @param thisZipFile A zipfile representing a student's project
        @returns nothing
        """

        project = StudentProjectCPP.StudentProjectCPP(filenames, self.tests)
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

        studentFiles = glob.glob('*.cpp')
        studentFiles.sort()

        numberProcessed = 0
        processFiles = False

        if self.limit == 0:
            self.limit = len(studentFiles)

        if self.selectStudent is None:
            processFiles = True

        for filename in studentFiles:

            if numberProcessed < self.limit and (
                processFiles or
                self.selectStudent is None or
                self.selectStudent in filename 
               ):
                self.processStudentProject([filename])
                processFiles = True
                numberProcessed += 1

                if self.weShouldPause:
                    input("Press enter to continue.")

        # Move up
        os.chdir("../")

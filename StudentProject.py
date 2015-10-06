import subprocess
import zipfile
import glob
import os
import os.path

"""
StudentProject will display files and execute projects in Java
provided that the project were created using the Eclipse structure.

Required commands: java, unzip (used by subprocess)
"""
class StudentProject:

    def __init__(self, myZipfile, mainClass=None, filesToInspect=[], classpath=None):
        """
        myZipfile: zipfile of the project
        mainClass: class containing the main method
        filesToInspect: list of files which will be displayed before execution.
        classpath: classpath which is passed to java.
        """

        self.myZipfile = myZipfile
        self.mainClass = mainClass
        self.filesToInspect = filesToInspect
        self.classpath = "../lib/acm.jar:."

        if classpath is not None:
            self.classpath = classpath

        folder = myZipfile.split(".")[0]
        folder = folder.replace(' ', '_')
        folder = folder.replace('(', '_')
        folder = folder.replace(')', '_')
        self.folder = folder

    def singleJUnitTest(self, jUnitClass):

        # Run the program
        jUnitClassPath = "/home/jcchurch/code/python/grading/junit.jar:"+self.classpath
        print(">> Testing:", jUnitClass)
        output = self.getProcessOutput(["java", "-cp", jUnitClassPath, "org.junit.runner.JUnitCore", jUnitClass])

        for line in output.split("\n"):
            if "tests" in line.lower():
                print(line)

    def performJUnitTests(self):

        if os.path.isdir("bin"):
            os.chdir("bin")

            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith("class"):
                        jUnitClass = root + "/" + file
                        jUnitClass = jUnitClass.replace("/", ".")
                        jUnitClass = jUnitClass.replace(".class", "")
                        jUnitClass = jUnitClass.replace("..", "")
                        self.singleJUnitTest(jUnitClass)

            # Return to the current working directory
            os.chdir("../")
        else:
            print("There's no bin directory in this project.")

    def unzipProject(self):
        """
        Unzips a student project to a new directory.
        """

        if os.path.isdir(self.folder) == False:
            os.mkdir(self.folder)

            if self.myZipfile.endswith("zip"):
                zipObject = zipfile.ZipFile(self.myZipfile, 'r')
                zipObject.extractall(path=self.folder)

        if self.myZipfile.endswith("tgz"):
            print(self.getProcessOutput(["tar", '-xzvf', self.myZipfile, '-C', self.folder]))

    def displayFile(self, filename):
        """
        Displays a filename.
        filename: the file to be displayed.
        """

        print("-"*80)
        print("##", filename)
        print("-"*80)
        print()

        if os.path.isfile(filename):
            self.getProcessOutput(["less",filename])
            subprocess.call(["less",filename])
            """
            f = open(filename, 'r', encoding="latin-1")
            for line in f:
                print(line, end='')

            print()
            print("-"*80)
            print("## END OF FILE")
            print()
            """

        else:
            print("!! File does not exist.")
            print()
        input("press enter to continue")

    def showFilesToInspect(self):
        """
        Displays all files to inspect (if any).
        """

        if len(self.filesToInspect) > 0:
            for filename in self.filesToInspect:
                self.displayFile(filename)

    def moveToProject(self):
        """
        We are currently in the folder containing all student projects
        and we move to the main folder inside a student's Eclipse
        project.
        """

        # Move to Project Folder
        os.chdir(self.folder)

        # There should be exactly one project in the folder
        projectDir = glob.glob('*')[0]

        # Move inside the student's Eclipse folder
        os.chdir(projectDir)

    def executeProject(self):
        """
        We execute the student project.
        """

        if self.mainClass is not None:
            # Check to see if 'bin' exists. Sometimes it won't
            # If the student was never able to get past the first
            # compile.
            if os.path.isdir("bin"):
                os.chdir("bin")

                # Run the program
                print("Executing student project:",self.folder)
                print(" ".join(["java", "-cp", self.classpath, self.mainClass]))
                self.getProcessOutput(["java", "-cp", self.classpath, self.mainClass])

                # Return to the current working directory
                os.chdir("../")
            else:
                print("There's no bin directory in this project.")

    def returnToBaseDirectory(self):
        """
        We return to the base directory containing all student zip files.
        We assume that we are in the base folder of the Eclipse project
        (and not the folder created to contain the Eclipse project.)
        """
        os.chdir("../..")

    def getProcessOutput(self, myCommand):
        call = subprocess.Popen(myCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        call.wait()
        (output, error) = call.communicate()
        decode = "BAD OUTPUT"
        try:
            decode = output.decode("utf-8")
        except UnicodeDecodeError:
            pass
        return decode

    def listAllJavaFiles(self):
        print("="*80)
        print("Listing of All Java Files")
        print(self.getProcessOutput("find . -name *.java".split()))
        print("="*80)

    def start(self):
        print("="*80)
        print("Inspecting", self.folder)
        print("="*80)
        self.unzipProject()
        self.moveToProject()
        self.showFilesToInspect()
        self.executeProject()
        # self.performJUnitTests()
        self.listAllJavaFiles()
        self.returnToBaseDirectory()
        print("="*80)
        print("Concluding", self.folder)
        print("="*80)

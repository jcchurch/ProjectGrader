"""StudentProjectJava represents a class of project objects."""

import StudentProject
import os
import os.path
import zipfile

class StudentProjectJava(StudentProject.StudentProject):
    """
    StudentProjectJava maintains a student's project.

    Required commands: java, unzip (used by subprocess)
    """

    def __init__(self, myZipfile, mainClass=None, filesToInspect=[], classpath=None):
        """
        Build the StudentProjectJava object.

        myZipfile: zipfile of the project
        mainClass: class containing the main method
        filesToInspect: list of files which will be displayed before execution.
        classpath: classpath which is passed to java.
        """
        folder = myZipfile.split(".")[0]
        folder = folder.replace(' ', '_')
        folder = folder.replace('(', '_')
        folder = folder.replace(')', '_')
        super().__init__(self, folder);

        self.myZipfile = myZipfile
        self.mainClass = mainClass
        self.filesToInspect = filesToInspect

        self.junitpath = "/home/jcchurch/code/python/ProjectGrader/junit-4.12.jar"
        self.hamcrestpath = "/home/jcchurch/code/python/ProjectGrader/hamcrest-core-1.3.jar"

        self.classpath = "../lib/acm.jar:."

        if classpath is not None:
            self.classpath = classpath

    def singleJUnitTest(self, jUnitClass):
        """Perform one unit test on jUnitClass."""
        testPath = self.junitpath+":"+self.hamcrestpath+":"+self.classpath+":."
        print(">> Testing:", jUnitClass)
        print(" ".join( ["java", "-cp", testPath, "org.junit.runner.JUnitCore", jUnitClass] ))
        output = self.getProcessOutput(["java", "-cp", testPath, "org.junit.runner.JUnitCore", jUnitClass])

        for line in output.split("\n"):
            if "tests" in line.lower():
                print(line)

    def performJUnitTests(self):
        """Perform unit testing on each file in a java project."""
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
        """Unzip a student project to a new directory."""
        if os.path.isdir(self.folder) == False:
            os.mkdir(self.folder)

            if self.myZipfile.endswith("zip"):
                zipObject = zipfile.ZipFile(self.myZipfile, 'r')
                zipObject.extractall(path=self.folder)

        if self.myZipfile.endswith("tgz"):
            print(self.getProcessOutput(["tar", '-xzvf', self.myZipfile, '-C', self.folder]))

    def showFilesToInspect(self):
        """Display all files to inspect (if any)."""
        if os.path.isdir("src"):
            os.chdir("src")

            for root, dirs, files in os.walk('.'):
                for aFile in files:
                    for filename in self.filesToInspect:
                        if aFile.endswith(filename):
                            self.displayFile(root +"/"+ aFile);

            # Return to the current working directory
            os.chdir("../")
        else:
            print("There's no src directory in this project.")

    def executeProject(self):
        """Execute the student project."""
        if self.mainClass is not None:
            # Check to see if 'bin' exists. Sometimes it won't
            # If the student was never able to get past the first
            # compile.
            if os.path.isdir("bin"):
                os.chdir("bin")

                # Run the program
                print("Executing student project:",self.folder)
                print(" ".join(["java", "-cp", self.classpath, self.mainClass]))
                print(self.getProcessOutput(["java", "-cp", self.classpath, self.mainClass]))

                # Return to the current working directory
                os.chdir("../")
            else:
                print("There's no bin directory in this project.")

    def returnToBaseDirectory(self):
        """
        Return to the base directory.

        We return to the base directory containing all student zip files.
        We assume that we are in the base folder of the Eclipse project
        (and not the folder created to contain the Eclipse project.)
        """
        os.chdir("../..")

    def start(self):
        """Start the process of examining a student's project."""
        print("="*80)
        print("Inspecting", self.folder)
        print("="*80)

        self.unzipProject()
        self.moveToProject()
        self.showFilesToInspect()
        self.executeProject()
        self.performJUnitTests()
        self.listAllFilesByExtension(self, "java");
        self.returnToBaseDirectory()
        print("="*80)
        print("Concluding", self.folder)
        print("="*80)

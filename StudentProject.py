"""StudentProject represents a class of project objects."""

import subprocess
import glob
import os
import os.path

class StudentProject:
    """
    StudentProject maintains a student's project.

    @param folder (which can be ignored)
    """

    def __init__(self, folder=""):
        """
        Build the StudentProject object.
        """
        self.folder = folder

    def displayFile(self, filename):
        """
        Display a filename.

        filename: the file to be displayed.
        """
        print("-"*80)
        print("##", filename)
        print("-"*80)
        print()

        if os.path.isfile(filename):
            f = open(filename, 'r', encoding="latin-1")
            for line in f:
                print(line, end='')

            print()
            print("-"*80)
            print("## END OF FILE")
            print()

        else:
            print("!! File does not exist.")
            print()

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

    def moveToProject(self):
        """
        Move to the project folder.

        We are currently in the folder containing all student projects
        and we move to the main folder inside a student's Eclipse
        project.
        """
        # Move to Project Folder
        os.chdir(self.folder)

        # Look for anything that isn't RemoteSystemsTempFiles
        for dirpath in glob.glob('*'):
            if dirpath != 'RemoteSystemsTempFiles':
                projectDir = dirpath

        # Move inside the student's Eclipse folder
        os.chdir(projectDir)

    def returnToBaseDirectory(self):
        """
        Return to the base directory.

        We return to the base directory containing all student zip files.
        We assume that we are in the base folder of the Eclipse project
        (and not the folder created to contain the Eclipse project.)
        """
        os.chdir("../..")

    def getProcessOutput(self, myCommand, instr=""):
        """Execute a process and returns the output of that process."""
        call = subprocess.Popen(myCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        (output, error) = call.communicate(input=instr)
        decode = "BAD OUTPUT"
        try:
            decode = bytes(output, 'utf-8').decode('utf-8', 'ignore')
        except UnicodeDecodeError:
            pass
        return decode

    def listAllFilesByExtension(self, extension):
        """Display a list of all files in all sub directories with extension."""
        print("="*80)
        print("Listing of All ", extension, "Files")
        cmd = "find . -name *."+extension
        print(self.getProcessOutput(extension.split()))
        print("="*80)

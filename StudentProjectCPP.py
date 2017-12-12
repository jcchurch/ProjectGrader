"""StudentProjectCPP represents a class of project objects."""

import StudentProject
import os
import os.path

class StudentProjectCPP(StudentProject.StudentProject):
    """
    StudentProjectCPP maintains a student's project.
    """

    def __init__(self, filenames, tests):
        """
        Build the StudentProjectCPP object.

        filenames: filenames of the project
        """
        self.filenames = filenames
        self.tests = tests

    def compile(self):
        print("Compling student project:", self.filenames[0])
        self.getProcessOutput(["g++", self.filenames[0]])

    def executeProject(self):
        """Execute the student project."""
        outfile = "./a.out"
        if os.path.isfile(outfile) == False:
            self.compile()

        if os.path.isfile(outfile) == True:
            # Run the program
            print("Executing student project:", self.filenames[0])

            i = 1
            for test in self.tests:
                print("Test #", i,"--", test)
                print(self.getProcessOutput([outfile], test))
                i += 1

            os.remove(outfile)
        else:
            print("Compiling error.")

    def start(self):
        """Start the process of examining a student's project."""
        print("="*80)
        print("Inspecting", self.filenames[0])
        print("="*80)
        self.displayFile(self.filenames[0])
        print("="*80)
        self.compile()
        self.executeProject()
        print("="*80)
        print("Concluding")
        print("="*80)

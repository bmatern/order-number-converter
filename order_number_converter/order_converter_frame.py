# This file is part of order-number-converter.
#
# order-number-converter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# order-number-converter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with order-number-converter. If not, see <http://www.gnu.org/licenses/>.


#from tkinter import Tk, filedialog, messagebox, Frame, StringVar, Label, Button, Entry, Scrollbar, Text, Toplevel
#from tkinter.constants import HORIZONTAL, BOTH, W, BOTTOM, X, Y, RIGHT, NONE, DISABLED, END, NORMAL

from tkinter import Frame, StringVar, Button, Entry, filedialog, Label
from tkinter.constants import BOTH, W, NORMAL, DISABLED

from os import makedirs, listdir
from os.path import split, abspath, join, pardir, basename, normpath, exists, isdir

#from datetime import today
import datetime

import sys

#import csv


class NumberConverterMasterFrame(Frame):
    def __init__(self, root):

        Frame.__init__(self, root)
        root.title("SeqPilot Order Number Fixer")

        self.parent = root
        self.initialize()


    # Initialize GUI elements
    def initialize(self):
        print('Setting up the GUI')


        # This is the directory the python executable is running from.
        FileAndPath = abspath(__file__)
        self.idir, self.ifile = split(FileAndPath)

        # GUI options
        #self.label_opt = {'fill': Tkconstants.BOTH, 'padx': 10, 'pady': 10}
        self.button_opt = {'fill': BOTH, 'padx': 50, 'pady': 15}

        # "Choose Directory" options change for windows and linux. In windows we want to default
        # to the swisslab directory.
        if (self.getPlatform() == 'Windows'):
            self.dir_opt = {'initialdir': "Z:\\bin\\TalkMaster\\Output\\Swisslab", 'mustexist': True,
                'parent': self, 'title': 'Choose a directory'}
        else:
            self.dir_opt = {'initialdir': "/home", 'mustexist': True,
                'parent': self, 'title': 'Choose a directory'}

        self.directoryFrame = self.makeDirectoryFrame()
        self.directoryFrame.pack()

        self.sampleFileFrame = self.makeSampleFileFrame()
        self.sampleFileFrame.pack()

        self.idChooserFrame = self.makeidChooserFrame()
        self.idChooserFrame.pack()

        self.pack()

    def makeDirectoryFrame(self):
        print('Setting up the directory Frame')

        chooseDirectoryFrame = Frame(self)

        self.chooseInputButton = Button(chooseDirectoryFrame, text='Kies Invoer Map', command=self.chooseInputDirectory)
        self.chooseInputButton.grid(row=0, column=0, sticky=W)

        #self.chooseOutputButton = Button(chooseDirectoryFrame, text='Choose Output Directory',
        #                                 command=self.chooseReadOutputDirectory)
        #self.chooseOutputButton.grid(row=1, column=0, sticky=W)
        self.outputDirLabel = Label(chooseDirectoryFrame, text="Output Map:")
        self.outputDirLabel.grid(row=1, column=0)


        self.inputDirectoryText = StringVar()
        self.inputDirectoryText.set('Waar zitten de bestanden?')
        Entry(chooseDirectoryFrame, width=80, textvariable=self.inputDirectoryText).grid(row=0, column=1)

        self.outputDirectoryText = StringVar()
        self.outputDirectoryText.set('Output Map')
        Entry(chooseDirectoryFrame, width=80, textvariable=self.outputDirectoryText).grid(row=1, column=1)
        #self.outputDirEntry.config(state=DISABLED)

        return chooseDirectoryFrame

    def makeSampleFileFrame(self):
        print('Setting up the directory Frame')

        sampleFileFrame = Frame(self)

        self.fileFoundLabelText = StringVar()
        self.fileFoundLabelText.set("Kies een map.")
        self.fileFoundLabel = Label(sampleFileFrame, textvariable=self.fileFoundLabelText)
        self.fileFoundLabel.pack()

        return sampleFileFrame

    def makeidChooserFrame(self):
        print('Setting up the directory Frame')

        idChooserFrame = Frame(self)

        self.changeIDButton = Button(idChooserFrame, text='Verander ID in:', command=self.changeID, state=DISABLED)
        self.changeIDButton.grid(row=0, column=0, sticky=W)


        self.newIDEntryText = StringVar()
        self.newIDEntryText.trace_add("write", self.changeNewIDMethod)
        self.newIDEntryText.set('new_id')# Underscores arent allowed, but the callback should change this to "-"
        Entry(idChooserFrame, width=50, textvariable=self.newIDEntryText).grid(row=0, column=1)

        self.skipFileButton = Button(idChooserFrame, text='Bestand Overslaan: ', command=self.skipFile, state=DISABLED)
        self.skipFileButton.grid(row=1, column=0, sticky=W)

        self.stopButton = Button(idChooserFrame, text='Stoppen.', command=self.skipAllFiles, state=DISABLED)
        self.stopButton.grid(row=1, column=1, sticky=W)

        return idChooserFrame

    def changeNewIDMethod(self, *args):
    # This method triggers when the new ID changes.
    # might be hand-typed or come from input from the barcode scanner.
    # Either way we should never allow underscores in the ID. Change "_" to "-"

        # *args are 3 parameters about who sent the callback. Not really important to me.
        #print('These args passed into the callback: ' + str(args))
        self.newIDEntryText.set(self.newIDEntryText.get().replace("_",'-'))


    # I borrowed this code from:
    # https://www.webucator.com/how-to/how-check-the-operating-system-with-python.cfm
    # Thanks Nat Dunn.
    def getPlatform(self):
        platforms = {
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OS X',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]


    # chooseInputDirectory method is called when the user presses the input directory button
    def chooseInputDirectory(self):
        print ('Choosing an input directory.')

        # File Dialog to get the new directory
        currentInputDirectory = filedialog.askdirectory(**self.dir_opt)
        # askdirectory returns an empty tuple when it fails.  Why? that seems dumb. String when successful.

        if(currentInputDirectory == "" or currentInputDirectory == None or currentInputDirectory == ()):
            print("Directory was not found, maybe you closed the window too early?")
        else:
            # Set the text object to new dir
            self.inputDirectoryText.set(normpath(currentInputDirectory))

            self.fileList = listdir(currentInputDirectory)
            self.currentFileIndex = 0
            print('These files found:' + str(self.fileList))

            # Parse the path to generate the output directory.
            parentDir = abspath(join(currentInputDirectory, pardir))
            leafDirName = basename(normpath(currentInputDirectory))
            todaysDate = datetime.date.today().strftime('%Y%m%d')
            # print ('todays date is: ' + str(todaysDate))
            currentOutputDirectory = join(parentDir, leafDirName + '_' + str(todaysDate) + '_fixed')
            self.outputDirectoryText.set(currentOutputDirectory)


            # If there are files in this directory
            if(len(self.fileList) > 0):
                # This output directory should exist
                if not exists(currentOutputDirectory):
                    makedirs(currentOutputDirectory)

                # Change the GUI to not allow us to change the directory. Enable the ID buttons.
                self.chooseInputButton.config(state=DISABLED)

                # Present a file to the user.
                self.presentAFile()


            else:

                messagebox.showwarning("No Files????", "There are no files in that directory. Try again.")


    def presentAFile(self):
        # Files Remaining? Nah I don't need to check i think.

        # Open File
        currentFile = self.fileList[self.currentFileIndex]
        currentFileFullPath = join(self.inputDirectoryText.get(), currentFile)
        with open(currentFileFullPath, 'r') as f:
            #reader = csv.reader(f, delimiter='\t')

            line = next(f)

            lineTokens = line.split('\t')

            # Get ID, it's the 2nd entry in a tab delimited file.
            self.oldSampleID = lineTokens[1]
            print ('I found this sampleid:' + str(self.oldSampleID))

        # Update Label with Instructions.  Filename, ID number.
        self.fileFoundLabelText.set("(" + str(self.currentFileIndex + 1) + "/" + str(len(self.fileList)) + ") " + str(currentFile) + "\n" +
            "heeft ID " + str(self.oldSampleID) + "\n" +
            "Fix ID of Overslaan?")

        self.changeIDButton.config(state=NORMAL)
        self.skipFileButton.config(state=NORMAL)
        self.stopButton.config(state=NORMAL)

        # Update Suggested new ID number.
        self.newIDEntryText.set(self.oldSampleID)


    def changeID(self):
        print('Changing the ID')

        # Open Input File
        currentFileFullPath = join(self.inputDirectoryText.get(), self.fileList[self.currentFileIndex])

        outputFileName = join(self.outputDirectoryText.get(), self.fileList[self.currentFileIndex])
        outputFile = createOutputFile(outputFileName)

        newSampleID = self.newIDEntryText.get()

        print('Replacing old id ' + str(self.oldSampleID) + ' with new id ' + str(newSampleID))

        with open(currentFileFullPath, 'r') as f:
            for line in f:
                newLine = line.replace(self.oldSampleID, newSampleID)
                outputFile.write(newLine)

        self.nextFilePlease()


    def skipFile(self):
        print('Skipping the File')
        # This method is just copying a file to the output directory.

        # Open Input File
        currentFileFullPath = join(self.inputDirectoryText.get(), self.fileList[self.currentFileIndex])

        outputFileName = join(self.outputDirectoryText.get(), self.fileList[self.currentFileIndex])
        outputFile = createOutputFile(outputFileName)

        with open(currentFileFullPath, 'r') as f:
            for line in f:
                outputFile.write(line)

        self.nextFilePlease()

    def skipAllFiles(self):
        while (self.currentFileIndex < len(self.fileList)):
            self.skipFile()

    def nextFilePlease(self):
        self.currentFileIndex += 1
        # More files Remaining?
        # Get the next file in the list.
        if (self.currentFileIndex < len(self.fileList)):
            self.presentAFile()
        # Else? finish up
        else:
            self.fileFoundLabelText.set("Kies een map.")

            self.chooseInputButton.config(state=NORMAL)
            self.changeIDButton.config(state=DISABLED)
            self.skipFileButton.config(state=DISABLED)
            self.stopButton.config(state=DISABLED)


# This method is a directory-safe way to open up a write file.
def createOutputFile(outputfileName):
    tempDir, tempFilename = split(outputfileName)
    if not isdir(tempDir):
        makedirs(tempDir)
    resultsOutput = open(outputfileName, 'w')
    return resultsOutput




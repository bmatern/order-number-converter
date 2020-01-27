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

from sys import argv
from getopt import getopt, GetoptError

from os.path import isfile, isdir, join

from order_number_converter.order_converter_frame import NumberConverterMasterFrame

from tkinter import Tk



def readArgs():

    # Trying to be consistent and global with my parameter inputs.

    # if(len(argv) < 5):
        #print ('I don\'t think you have enough arguments.\n')
        #usage()
        #return False

    # print('Loading commandline arguments')
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    try:
        opts, args = getopt(argv[1:]
            ,"hvi:o:p:n:"
            ,["help","version","inputdir=", "outputdir=", "previousordernumber=", "newordernumber="])

        print (str(len(opts)) + ' arguments found.')

        for opt, arg in opts:

            if opt in ('-h', '--help'):
                #print (SoftwareVersion)
                #usage()
                return False

            elif opt in ('-v', '--version'):
                #print (SoftwareVersion)
                return False

            else:
                print('Unknown Commandline Option:' + str(opt) + ':' + str(arg))
                raise Exception('Unknown Commandline Option:' + str(opt) + ':' + str(arg))
            

    except GetoptError as err:
        print ('Something seems wrong with your commandline parameters.')
        print (str(err.msg))
        print ('Unknown option: ' + str(err.opt))
        return False

    return True


if __name__=='__main__':
    readArgs()


    root = Tk()
    app = NumberConverterMasterFrame(root)
    root.mainloop()

    print('Done.  Great.')

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

#!/usr/bin/env python

"""
@author David Stuebe <dstuebe@asascience.com>

A demo executable to write or read data in an hdf file using pytables Extendable Array Type

run with:
python pytables_process.py <FLAG>

where FLAG is either "writer" or "reader"
for example:

python pytables_process.py writer


Alternatively - use the subprocess_script to automate a concurrent test with a number of readers....

"""


from numpy import *
from tables import *


def writer(file, dset):

    # Type of atom in the extendable array
    a = UInt64Atom()

    # Open a new empty HDF5 file
    fileh = openFile(file, mode = "a")
    # Get the root group
    group = fileh.root

    try:
        hdf_array = getattr(group, dset)
    except NoSuchNodeError:
        hdf_array = fileh.createEArray(group, dset,a,(0,100,100),"Appendable list of unsigned integers")

    base = ones([100,100],uint8)
    hdf_array.append([base * i for i in xrange(10)])

    # Close the file
    fileh.close()

def reader(file, dset):

    fileh = openFile(file,mode='r')

    group = fileh.root

    hdf_array = getattr(group, dset)

    print 'Current array shape: ', hdf_array.shape

    a = hdf_array[0,:,:]
    b = hdf_array[hdf_array.nrows-1,:,:]

    print a[0], b[0]


    fileh.close()



if __name__ == '__main__':
    import sys

    fname = 'test_file.h5'

    dset = 'dataset1'

    iterations = 20


    flag = None
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        print 'Got Flag: "%s"' % flag

    if flag == "writer":

        for i in xrange(iterations**2):
            writer(fname,dset)
            if i%iterations == 0:
                print 'Writer iteration: ', i

    elif flag == "reader":

        for i in xrange(iterations):
            reader(fname, dset)

    else:
        raise RuntimeError('Bad flag passed to concurrent test.')



    exit(0)


#!/usr/bin/env python

"""
@author David Stuebe <dstuebe@asascience.com>


To Run:
bin/python subprocess_script.py
"""

import subprocess
import time

if __name__ == '__main__':


    subprocess_pool = list()
    open_files = list()

    pool_size = 5

    for i in xrange(pool_size):
        print 'starting subprocess %d' % i
        job = 'python'

        arg = 'pytables_process.py'

        proc = [job, arg]
        if i==0:
            proc.append('writer')
            sleep_time = 0.5
        else:
            proc.append('reader')
            sleep_time = 0

        f = open('/tmp/g%s'%i, 'w')
        out = f.fileno()
        open_files.append(f)

        subprocess_pool.append(subprocess.Popen(proc, shell=False, stdout=out, stderr=out))
        time.sleep(sleep_time)



    for process in subprocess_pool:

        process.wait()
    for f in open_files:
        f.close()


    print "TADA!"

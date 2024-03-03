#!/usr/bin/env python

import pickle
from io import StringIO
import sys
import qckt
import qckt.noisemodel as ns
import qckt.backend as bknd
from flask import Flask, request, jsonify
from multiprocessing import Process
import os

app = Flask(__name__)

def runjob_worker(job):

    # get a handle on the backend engine
    bk = bknd.DMQeng()

    # redirect stdout, stderr to capture them
    # THIS IS NOT THREAD SAFE !!! All threads share the same sys.stdout so will write into this same StringIO
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = mystdout = StringIO()
    sys.stderr = mystderr = StringIO()

    # run the job with the stdout and stderr captured
    bk.runjob(job)

    # revert the stdout and stderr to original values
    sys.stderr = old_stderr
    sys.stdout = old_stdout

    # package the result, runstats, and stdout, stderr outputs
    retval = {'result':job.result, 'runstats':job.runstats, 'stdout':mystdout.getvalue(), 'stderr':mystderr.getvalue()}
    retval_pkl = pickle.dumps(retval)

    # return the result
    return retval_pkl, 200

@app.route('/runjob', methods=['POST'])
def runjob():
    # extract job object from request
    payload = request.get_data()
    job = pickle.loads(payload)
    retval_pkl, ret_status = runjob_worker(job)

    p = Process(target=runjob_worker, args=(job,))
    p.start()
    print('Main thread')
    p.join()

    return retval_pkl, ret_status

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
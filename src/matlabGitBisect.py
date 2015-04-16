#!/usr/bin/python
# encoding: utf-8
'''
matlabGitBisect -- a git bisect run script for Matlab projects

@author:     Twan Koolen
'''

import sys
import signal
import os
import subprocess

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2015-03-31'
__updated__ = '2015-03-31'

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

#     program_name = os.path.basename(sys.argv[0])
#     program_version = "v%s" % __version__
#     program_build_date = str(__updated__)
#     program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Twan Koolen on %s.
  Copyright 2015. All rights reserved.

  Licensed under MIT License

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    skipReturnCode = 125
    abortBisectReturnCode = 255
    
    buildSubProcess = None
    testSubProcess = None
    try:        
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-bc", "--build-code", dest="buildCode", help="code to build before running", default=None)
        parser.add_argument("-bd", "--build-dir", dest="buildDir", help="build directory", default=os.getcwd())
        parser.add_argument("-t", "--test-code", dest="testCode", help="test code to run", default="")
        parser.add_argument("-be", "--build-error-behavior", dest="buildErrorBehavior", default="bad", choices=['bad', 'skip'], help="behavior when a build error is detected.")
        parser.add_argument("-c", "--crash-behavior", dest="crashBehavior", default="bad", choices=['bad', 'skip'], help="behavior when a crash is detected")

        # Process arguments
        args = parser.parse_args()
        
        # Set up return codes 
        buildErrorReturnCode = {'bad': 3, 'skip': skipReturnCode}[args.buildErrorBehavior]
        crashedReturnCode = {'bad': 4, 'skip': skipReturnCode}[args.crashBehavior]
        
        # Build
        if args.buildCode is not None:
            print "Building..."
            buildSubProcess = subprocess.Popen(args.buildCode.split(), shell=True, cwd=args.buildDir, preexec_fn=os.setsid)
            buildSubProcess.wait()
            buildSubProcessReturnCode = buildSubProcess.returncode
            buildSubProcess = None
            if buildSubProcessReturnCode is not 0:
                print "Build failed"
                return buildErrorReturnCode
            else:
                print "Build done."
        
        # Run test
        resultsFileName = os.path.join(os.getcwd(), "results.txt")
        logFileName = os.path.join(os.getcwd(), "matlabGitBisectLog.txt")
        matlabFileDirectory = os.path.dirname(os.path.realpath(__file__))
        matlabCall = ["matlab", "-logfile", logFileName, "-nodesktop", "-nosplash", "-r", "runTest(\'" + resultsFileName + "\', \'" + args.testCode +"\')"]
        print "Running test..."
        testSubProcess = subprocess.Popen(matlabCall, cwd=matlabFileDirectory, stdin=subprocess.PIPE)
        testSubProcess.wait()
        print "Test done."
        testSubProcess = None
        crashed = not os.path.isfile(resultsFileName)
        
        # Process test results
        if crashed:
            print "Crashed!"
            return crashedReturnCode
        else:
            with open(resultsFileName, 'r') as f:
                testReturnCode = f.read()
            os.remove(resultsFileName)
            return testReturnCode

    except:
        print "Exiting matlabGitBisect."
        if buildSubProcess is not None:
            print "Killing build subprocess."
            os.killpg(buildSubProcess.pid, signal.SIGTERM) 
        if testSubProcess is not None:
            print "Killing test subprocess."
            testSubProcess.kill()
            testSubProcess.communicate()
        return abortBisectReturnCode

if __name__ == "__main__":
    sys.exit(main())

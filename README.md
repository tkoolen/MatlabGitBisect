# MatlabGitBisect

```
matlabGitBisect -- a git bisect run script for Matlab projects

  Created by Twan Koolen on 2015-03-31.
  Copyright 2015. All rights reserved.

  Licensed under TODO

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE

optional arguments:
  -h, --help            show this help message and exit
  -bc BUILDCODE, --build-code BUILDCODE
                        code to build before running
  -bd BUILDDIR, --build-dir BUILDDIR
                        build directory
  -t TESTCODE, --test-code TESTCODE
                        test code to run
  -be {bad,skip}, --build-error-behavior {bad,skip}
                        behavior when a build error is detected.
  -c {bad,skip}, --crash-behavior {bad,skip}
                        behavior when a crash is detected
```

Example usage to find where `testThisAndThat` started causing Matlab crashes, skipping revisions that resulted in build errors:
```
git bisect start
git bisect bad
git bisect good 9dea818feee7673084457356dfd034ad2f1a1e75
git bisect run ~/code/MatlabGitBisect/src/matlabGitBisect.py -bc "make -j" -bd .. -t "cd ~/code/MyProject;testThisAndThat;" -be skip -c bad

```

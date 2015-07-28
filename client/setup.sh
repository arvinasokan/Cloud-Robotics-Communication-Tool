#!/bin/bash
exitfn () {
    trap SIGINT              # Resore signal handling for SIGINT
    exit                     #   then exit script.
}
trap "exitfn" INT
SCRIPTPATH=$(dirname "$SCRIPT")
cd $SCRIPTPATH
cd dependencies
cd pycrypto-2.6.1
python setup.py build
sudo python setup.py install
cd ..
cd xlwt-1.0.0
python setup.py build
sudo python setup.py install
cd ..



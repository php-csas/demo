#!/bin/bash

dir=`pwd`

# Check if the appropriate commands exist
if ! command_exists vagrant ; then
    echo "Vagrant does not exist on this machine. The demonstration needs Vagrant to run the demonstration site. Aborting."
    exit 1
fi

if ! command_exists python ; then
    echo "Python does not exist on this machine. The demonstration needs Python for the XSS injection into the demonstration site to work. Aborting."
    exit 1
fi

cd no_csas && vagrant up
cd ${dir}

while true; do
    echo "Running demonstration with csas NOT enabled"
    # Run the Python script to do the XSS injections
    python xss_demo.py --url http://localhost:8082
    # Reboot the Vagrant machine when the demo is done
    # cd csas && vagrant reload
done


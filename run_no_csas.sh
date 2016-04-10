#!/usr/bin/env bash

dir=`pwd`

cd no_csas && vagrant up
cd ${dir}

# while true; do
#    echo "Running demonstration with csas NOT enabled"
    # Run the Python script to do the XSS injections
#    python xss_demo.py --url http://localhost:8082
    # Reboot the Vagrant machine when the demo is done
    # cd csas && vagrant reload
# done

echo "Running demonstration with csas NOT enabled"
# Run the Python script to do the XSS injections
python xss_demo.py --url http://localhost:8082
# Reboot the Vagrant machine when the demo is done
# cd csas && vagrant reload


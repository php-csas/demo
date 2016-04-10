#!/usr/bin/env bash

dir=`pwd`

cd csas && vagrant up
cd ${dir}

# while true; do
#    echo "Running demonstration with csas enabled"
    # Run the Python script to do the XSS injections
#    python xss_demo.py --url http://localhost:8081
    # Reboot the Vagrant machine when the demo is done
    # cd csas && vagrant reload
# done

echo "Running demonstration with csas enabled"
# Run the Python script to do the XSS injections
python xss_demo.py --url http://localhost:8081
# Reboot the Vagrant machine when the demo is done
# cd csas && vagrant reload



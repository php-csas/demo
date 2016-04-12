#!/usr/bin/env bash

dir=`pwd`

cd no_csas && vagrant up --provision

while true; do
    vagrant ssh -c 'mysql -uroot -pcsas -e "USE csas; TRUNCATE TABLE post;"'
    echo "Running demonstration with csas NOT enabled"
    # Run the Python script to do the XSS injections
    python ${dir}/xss_demo.py --url http://localhost:8082
done


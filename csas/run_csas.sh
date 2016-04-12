#!/usr/bin/env bash

dir=`pwd`

cd csas && vagrant up --provision

while true; do
    vagrant ssh -c 'mysql -uroot -pcsas -e "USE csas; TRUNCATE TABLE post;"'
    echo "Running demonstration with csas enabled"
    # Run the Python script to do the XSS injections
    python ${dir}/xss_demo.py --url http://localhost:8081
done


#!/bin/bash

ROWS_NUMBER=4
COLS_NUMBER=4
DEBUG=false

python3 app/main.py --rows_number=$ROWS_NUMBER --cols_number=$COLS_NUMBER --debug=$DEBUG

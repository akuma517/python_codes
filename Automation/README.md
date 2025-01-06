# Automation Code
The script allows the user to switch between two windows automatically.

## Run Environment:
    Linux

## Description:
Loops switching between the two open window in linux environment. 
The name and duration of switch for both windows is configurable.
To exit the loop, PRESS 'ESC'.

## Dependencies:
    - pynput  # pip install pynput
    - wmctrl  #sudo apt-get install wmctrl

## How to run?
    - python3 ./automatic_window_switching.py -w1 "<title1>" -t1 <time1> -w2 "<title2>" -t2 <time2>
      Eg. python3 ./automatic_window_switching.py -w1 "Untitled Document" -t1 4 -w2 "Terminal" -t2 2
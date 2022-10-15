# PerfTracker

## Goal
The goal of this program is to test the speeds of different programs both by looking at programs individually, or comparing them between each other. 

## Logic

Logically, there is a timer and a program object.

The timer objects are designed in a tree structure (to time different subroutines of the programs). 

The program object runs a program and tracks its main timer.


## Usage

perftracker has different command line options:

    -n name

    -o output folder

    -i number of iterations per program (times are averaged)

    -v generate valgrind output

    -g generate example config file

    -f config file (listig out the programs to compare)

    -p program to run (overrides any config file and assumes only one program is being tested)

## Understanding the output

Everything gets outputted to the output folder under the name.

For example, all the data will be written to `./output_folder/name/`

Within this folder, there are subfolders for every program being tested, and one for the comparisons. 

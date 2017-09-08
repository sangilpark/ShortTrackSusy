#!/bin/bash
#
# created 8.06.17 by me
# 1st arg is input file that is being altered, 2nd argument is a name of backup copy file
#
OLD="'\/store"
NEW="'root:\/\/cmsxrootd\.fnal\.gov\/\/store\/"
#NEW="umaguma"
TFILE=$1
TFILE_2=$2
 
cp $TFILE $TFILE_2
sed -i "s/$OLD/$NEW/g" $TFILE

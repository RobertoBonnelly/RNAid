#!/usr/bin/bash


for i in $1*
do
    2ndscore --no-rvs $i > ../Dataset/$i.out
done
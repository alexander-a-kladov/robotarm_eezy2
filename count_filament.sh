#!/bin/bash
s=0
for a in `ls EBA*`
do b=`cat $a | grep 'Filament used:' | gawk -F ':' '{print $2}' | gawk -F '.' '{print $1}'`
s=`expr $s + $b + 1`
done
echo $s


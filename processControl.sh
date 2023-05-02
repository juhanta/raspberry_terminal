#!/bin/bash
while ((1)) ; do
stat1=$(ps -aef | grep '/home/user/Desktop/[l]ogin.py')
stat2=$(ps -e | grep '[c]hromium')
if [ -z "$stat1" ] && [ -z "$stat2" ]; then
/usr/bin/python3 /home/user/Desktop/login.py;
fi
done

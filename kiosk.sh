#!/bin/bash
xset s noblank
xset s off
xset -dpms

/usr/bin/chromium-browser --noerrdialogs --disable-infobars https://google.ee &

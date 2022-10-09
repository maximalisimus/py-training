#!/bin/bash
volumes=$(pactl get-sink-volume @DEFAULT_SINK@ | sed '2,$d' | awk '{print $5,$12}')
./window.py "Volume is: ${volumes[*]}"

exit 0

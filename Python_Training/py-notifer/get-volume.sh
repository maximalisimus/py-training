#!/bin/bash
volumes=$(pactl get-sink-volume @DEFAULT_SINK@ | sed '2,$d' | awk '{print $5,$12}')
echo "${volumes[*]}"

exit 0

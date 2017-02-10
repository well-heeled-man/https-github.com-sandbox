#!/bin/bash
#
# This script processes the performance data collected by the vscsiStats.py script.
#
# It should be ran from the same directory as the GZIP'ed files (but will not work on the ESXi itself).
#
# By default it generates a file called Processed_vscsiStats.csv. It processes the files in-place, so the individual files become useless and are deleted. BACK THEM UP.
#

# Gunzip all files.
gunzip *.gz

# Define the files for processing.
files=(vscsiStats_*)

# Create the template file.
awk '/Histogram/ {gsub(/,/,"|")} 1' ${files[0]} | awk -F ',' '{print $2","$1}' | sed -e 's/,H/H/g' | cut -d ',' -f1 | sed -e '/[0-9])/a\ ' > vscsiStats_00

# Cut the stat data from each line and rewrite in-place.
for i in "${files[@]}"; do echo "`cut -d ',' -f1 $i | sed -r "s/Histogram.*/\n$i/g"`" > $i; done

# Paste the collected statistics horizontally and clean up the final output.
paste -d ',' vscsiStats_* > Processed_vscsiStats.csv
sed -i -e "s/,,*/,/g" -e 's/),/)/g' -e 's\vscsiStats_\\g' -e 's\%3A\:\g' Processed_vscsiStats.csv

# Delete the processed files.
rm vscsiStats_*

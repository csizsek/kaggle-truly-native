#! /bin/bash

if [ $# -ne 2 ]
then
    echo "usage:
$> ./generate_features.sh <input_dir> <output_dir>
<input_dir>: the directory containing 0.zip, 1.zip, etc
<output_dir: the directory where the output files 0.csv, 1.csv, etc will be created"
    exit 1
fi

input_dir=$1
output_dir=$2

for i in 0 1 2 3 4 5
do
    unzip "$input_dir/$i.zip" -d "$input_dir"
    python generate_features.py "$input_dir/$i/" "$output_dir/$i.csv"
    rm -rf "$input_dir/$i/"
done

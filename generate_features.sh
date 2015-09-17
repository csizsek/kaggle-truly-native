#! /bin/bash -ex

input_dir=$1
output_dir=$2

for i in 0 1 2 3 4
do
    unzip "$input_dir/$i.zip" -d "$input_dir"
    python generate_features.py "$input_dir/$i/" "$output_dir/$i.csv"
    rm -rf "$input_dir/$i/"
done


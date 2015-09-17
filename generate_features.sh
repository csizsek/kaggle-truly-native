#! /bin/bash -ex

input_dir=$1
output_dir=$2

for i in 0 1 2 3 4 5
do
    unzip "$target_dir/$i.zip" -d "$target_dir"
    python generate_features.py "$target_dir/$i/" "$output_dir/$i.csv"
    rm -rf "$target_dir/$i/"
done


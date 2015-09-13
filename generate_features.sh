#! /bin/bash -ex

target_dir=$1

for i in 0 1 2 3 4
do
    unzip "$target_dir/$i.zip" -d "$target_dir"
    python generate_features.py "$target_dir/$i/" "$target_dir/$i.csv"
    rm -rf "$target_dir/$i/"
done


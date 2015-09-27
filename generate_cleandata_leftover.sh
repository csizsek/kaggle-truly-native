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
    N=$(wc -l "$output_dir"/clean"$i".txt | awk '{print $1}')
    unzip "$input_dir/$i.zip" -d "$input_dir"
    parser "$input_dir/$i/" stopwords.txt $N 1> "$output_dir"/clean"$i"_leftover.txt 2>> err
    rm -rf "$input_dir/$i/"
done

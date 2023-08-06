#!/bin/sh


# Set Paths for arguments
homeDir=$HOME
dataPath=${homeDir}/spa.txt
modelCheckPointPath="${homeDir}/export_model"
metricsPath="${homeDir}/metrics"
config='seq2seq.json'
n_epoch=20

# Change to repo directory
codeDir="${homeDir}/tangiblemt"
cd ${codeDir}

echo "$config" "$n_epoch" "$dataPath" "$modelCheckPointPath" "$metricsPath"

# Run Script
nmt --config "$config" --epoch "$n_epoch" --data_path "$dataPath" --model_checkpoint_dir "$modelCheckPointPath" --metrics_dir "$metricsPath"

#!/bin/bash


source activate fwei_py36 #使用tensorflow-gpu

set -x

#todo: 判断$1 是否为数字
if [ x$1 = x'' ]; then
  CUDA_DEVICE_INDEX=0
else
  CUDA_DEVICE_INDEX="$1"
fi

export CUDA_VISIBLE_DEVICES=$CUDA_DEVICE_INDEX

cd "$(dirname $0)" || exit 1 
cur_dir=$(pwd)

export BERT_BASE_DIR="$cur_dir"/model/chinese_L-12_H-768_A-12 # or multilingual_L-12_H-768_A-12
export STAR_DATA_DIR="$cur_dir"/star_data/

time python run_classifier.py \
  --task_name=STAR \
  --do_predict=true\
  --data_dir=$STAR_DATA_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint="$cur_dir"/star_output/train_output_model/model.ckpt-56250 \
  --max_seq_length=256 \
  --output_dir="$cur_dir"/star_output/test_output

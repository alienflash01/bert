# workflow

## 官方使用指南

### 预训练模型

使用[BERT-Base, Chinese](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)这个预训练模型

> if your fine-tuning data is Chinese-only, then the Chinese model will likely produce better results.(如果只是对中文分类，建议使用Chinese model)

### 官方数据集

[XNLI dataset](https://github.com/facebookresearch/XNLI)数据集，该数据集的dev 和测试集已经被（人工）翻译为15种语言，训练集是由机器翻译的（bert使用的是由XNLI提供的翻译），论文中提供了6中语言的测试结果。

### 怎样fine-tuning(使用官方的源码和数据集)

1. 下载[XNLI dev/test set](https://s3.amazonaws.com/xnli/XNLI-1.0.zip)和[XNLI train set](https://s3.amazonaws.com/xnli/XNLI-MT-1.0.zip)，然后解压`.zip`文件到`$XNLI_DIR`，这个目录会在运行`run_classifier.py`作为`--data_dir`的参数。
2. XNLI 数据集已经在`run_classifier.py`中" hard-coded "了，默认为中文，如果想要运行其他的语言，需要修改`XnliProcessor`
3. XNLI 是一个巨大的数据集，如果想要debug的话，可以设置`num_train_epochs`为一个小的值（比如0.1）
4. 训练使用的参数例子

    ```shell
    export BERT_BASE_DIR=/path/to/bert/chinese_L-12_H-768_A-12 # or multilingual_L-12_H-768_A-12
    export XNLI_DIR=/path/to/xnli

    python run_classifier.py \
    --task_name=XNLI \
    --do_train=true \
    --do_eval=true \
    --data_dir=$XNLI_DIR \
    --vocab_file=$BERT_BASE_DIR/vocab.txt \
    --bert_config_file=$BERT_BASE_DIR/bert_config.json \
    --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
    --max_seq_length=128 \
    --train_batch_size=32 \
    --learning_rate=5e-5 \
    --num_train_epochs=2.0 \
    --output_dir=/tmp/xnli_output/
    ```

## 实现一个自己的文本多分类的例子

### requirtments

#### 下载代码

这里fork了官方的代码，并且新建了一个 "star" 分支，使用如下命令获取代码：

```shell
git clone https://github.com/alienflash01/bert.git -b star
```

#### 下载预训练模型

下载使用[BERT-Base, Chinese](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip) 预训练模型，并解压放到 `./model`目录下。

```shell
wget https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip
#当然，可能在服务器上会404，自己想办法吧
```

#### 安装代码运行环境

依赖的环境包括：

- python3(貌似官方推荐Python2)
- tensorflow >= 1.11.0 (使用CPU)
- tensorflow-gpu >= 1.11.0 (使用GPU)

### fune-tuning 模型，进行一个文本分类任务

#### 数据处理

1. 将数据保存为如下格式：

    ```text
    game APEX是个新出的吃鸡游戏
    ```

    即分割为 "标签" + `tab` + "正文" 的形式。
2. 数据集放在`bert/star_data`目录下，涉及到的文件有：
    - star_train.tsv
    - star_dev.tsv
    - star_test.tsv
    - label.tsv, 该文件里面保存所有的标签（一行一个）
3. 进入到star_data 目录下，使用dataProcess.py可以生成需要的文件。

#### 修改代码

1. 添加一个StarProcessor 类，需要分别实现`get_train_examples`、`get_dev_examples`、`get_test_examples`、`get_labels`、`_create_examples`方法

#### 训练模型

直接使用`run.sh`文件，需要修改参数调参（todo）
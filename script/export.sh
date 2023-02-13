#!/bin/bash

# run
EXE=darknet
PYTHON=python3
NODE=node

# path
DATASET=$EAIFDK_HOME/dataset
BACKUP=$DATASET/backup
IMAGES=$DATASET/images
TOOLS=$EAIFDK_HOME/tools
BOARD=$EAIFDK_HOME/board
MODEL=$EAIFDK_HOME/model
QUAN=$EAIFDK_HOME/quantification
WEIGHTS=$DATASET/backup/
SAMPLES=$EAIFDK_HOME/samples
SAMPLES_SINGLECHIP=$SAMPLES/singlechip
TEST=$EAIFDK_HOME/test
NETWORK=$EAIFDK_HOME/network
DARKNET_DIR=$NETWORK/darknet
DEMO=$EAIFDK_HOME/demo
PREDITION=$EAIFDK_HOME/predition

# file
#dataset
DATA=$DATASET/data/collection.data
TRAIN=$DATASET/train/train.txt
VALID=$DATASET/valid/valid.txt
NAME=$DATASET/name/label.txt
CFG=$DATASET/cfg/weights.cfg
WEIGHTS_LAST=$WEIGHTS/weights_last.weights
#tools
AUTO_LABEL=$TOOLS/auto_label/main.py
AUTO_LABEL_MODEL=$TOOLS/auto_label/model.h5
UN_NAME=$TOOLS/unified_dataset_name.py
NETRON=$TOOLS/netron/source/server.py
#board
DAR2BOARD=$BOARD/darknet_to_board.py
IOU2AVG=$BOARD/iou_to_avg.py
LOSS2AVG=$BOARD/loss_to_avg.py
BOARD_START=$BOARD/starrt.js
BOARD_JS=$BOARD/server.js
#quantification
WEIGHTS2H5=$QUAN/yolo_to_h5.py
H52PB=$QUAN/h5_to_pb.py
PB2TFLITE=$QUAN/pb_to_tflite.py
#SAMPLES
SAMPLES_EMBEDDED_CLIENT=$SAMPLES/mbedded/client
#HOME
TEST_DEMO=$DEMO/face.jpg
#PREDITION
H5_PR=$PREDITION/h5_predition.py
PB_PR=$PREDITION/pb_prediction.py
TFLITE_PR=$PREDITION/tflite_prediction.py
#TEST
TEST_START=$TEST/start.js
TEST_JS=$TEST/server.js

# config
#class
CLASS_NAME=Face
#local
LOCAL_IP=172.18.0.7
#board
BOARD_PORT=8080
#NETRON_PORT
NETRON_PORT=8080
#test
TEST_PORT=8080

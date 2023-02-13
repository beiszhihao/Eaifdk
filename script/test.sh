#!/bin/bash

. $EAIFDK_HOME/script/export.sh

rm $TEST/images/*
cd $DARKNET_DIR

$EXE detector test $DATA $CFG $MODEL/$CLASS_NAME.weights $TEST_DEMO
mv predictions.jpg $TEST/images/test_weights.jpg

cd $EAIFDK_HOME

$PYTHON $H5_PR $MODEL/$CLASS_NAME.h5 $TEST_DEMO
mv dashen_compressed.jpg $TEST/images/test_h5.jpg

$PYTHON $PB_PR $MODEL/$CLASS_NAME.pb $TEST_DEMO
mv dashen_compressed_pb.jpg $TEST/images/test_pb.jpg

$PYTHON $TFLITE_PR $MODEL/$CLASS_NAME.tflite $TEST_DEMO
mv dashen_compressed_tflite.jpg $TEST/images/test_tflite.jpg

rm $TEST_START
sed 's/xxx.xxx.xxx.xxx/'$LOCAL_IP'/;s/0000/'$TEST_PORT'/' $TEST_JS > $TEST_START
node $TEST_START

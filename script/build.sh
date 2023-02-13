#!/bin/bash
. $EAIFDK_HOME/script/export.sh

if [ $CLASS_NAME = '' ];then
	echo "Do you forget efdk --update?"
	exit
fi

rm $MODEL/*
$PYTHON $WEIGHTS2H5 $CFG $WEIGHTS_LAST $MODEL/$CLASS_NAME.h5
$PYTHON $H52PB $MODEL/$CLASS_NAME.h5 $MODEL $CLASS_NAME.pb
$PYTHON $PB2TFLITE $IMAGES $MODEL/$CLASS_NAME.pb $MODEL/$CLASS_NAME.tflite
cp $WEIGHTS_LAST $MODEL/$CLASS_NAME.weights

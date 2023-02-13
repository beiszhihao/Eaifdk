#!/bin/bash

. $EAIFDK_HOME/script/export.sh

rm $BOARD/train_output.txt
rm $BACKUP/*
$EXE detector train $DATA $CFG |& tee $BOARD/train_output.txt

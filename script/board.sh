#!/bin/bash

. $EAIFDK_HOME/script/export.sh

rm $BOARD/images/*.png

$PYTHON $DAR2BOARD

LIN=$(wc -l $BOARD/train_log_loss.txt)

$PYTHON $LOSS2AVG $LIN

sed 's/.*iou_loss//g' $BOARD/train_log_iou.txt > $BOARD/a.tmp
sed 's/,.*//g' $BOARD/a.tmp > $BOARD/b.tmp
sed 's/=//' $BOARD/b.tmp > $BOARD/c.tmp
sed 's/[[:space:]]//g' $BOARD/c.tmp > $BOARD/d.tmp

$PYTHON $IOU2AVG d.tmp

rm $BOARD_START
rm $BOARD/train_log_loss.txt
rm $BOARD/*.tmp

sed 's/xxx.xxx.xxx.xxx/'$LOCAL_IP'/;s/0000/'$BOARD_PORT'/' $BOARD_JS > $BOARD_START
node $BOARD_START

#!/bin/bash

. $EAIFDK_HOME/script/export.sh

if [ "$1" == "" ];
then
	echo "Pless input class"
	exit
fi

rm $TRAIN $VALID $NAME $DATA

cd $DATASET
realpath $IMAGES/*.jpg > $TRAIN
cp $TRAIN $VALID
c=`awk -v x=2.45 -v y=3.123 'BEGIN{printf "%.2f\n",x*y}'`
count=$(cat $VALID | wc -l)
retain=`awk -v x=$count -v y=0.1 'BEGIN{printf "%d\n",x*y}'`
number=`awk -v x=$count -v y=$retain 'BEGIN{printf "%d\n",x-y}'`
sed -i '1,'$number'd' $VALID
add=`awk -v x=$number -v y=1 'BEGIN{printf "%d\n",x+y}'`
sed -i $add,$count'd' $TRAIN

sed -i -e "s:CLASS_NAME=.*:CLASS_NAME=$1:g" $EAIFDK_HOME/script/export.sh
echo $1 > $NAME
echo "classes = 1" > $DATA
echo "train = "$TRAIN >> $DATA
echo "valid = "$VALID >> $DATA
echo "names = "$NAME >> $DATA
echo "backup = "$BACKUP >> $DATA

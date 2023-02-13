#!/bin/bash

. $EAIFDK_HOME/script/export.sh

if [ '$1' == '--help' ];
then
	echo "view.sh [model_path]"
	exit
fi

$PYTHON $NETRON $1 $LOCAL_IP $NETRON_PORT

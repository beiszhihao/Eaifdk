#!/bin/bash

. $EAIFDK_HOME/script/export.sh

$EXE detector recall $DATA $CFG $WEIGHTS

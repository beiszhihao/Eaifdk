#!/bin/bash

. $EAIFDK_HOME/script/export.sh

$EXE detector map $DATA $CFG $WEIGHTS

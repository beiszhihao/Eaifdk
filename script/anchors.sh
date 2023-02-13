#!/bin/bash

. $EAIFDK_HOME/script/export.sh

$EXE detector calc_anchors $DATA -num_of_clusters 3 -width 56 -height 56
rm anchors.txt
rm counters_per_class.txt

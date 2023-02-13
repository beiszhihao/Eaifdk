#!/bin/bash

. $EAIFDK_HOME/script/export.sh

if [ $1 = 'embedded' ]; then
	cd $SAMPLES_EMBEDDED_CLIENT
	$NODE install
	if [ $? -ne 0 ]; then
		echo "Failed to build embedded sample project"
		exit
	fi
	echo "Build done."
fi

if [ $1 = 'singlechip' ]; then
        cd $SAMPLES_SINGLECHIP/arch/arm/stm32/stm32f746g_disco/server
	make
        if [ $? -ne 0 ]; then
                echo "Failed to build singlechip sample project"
                exit
        fi
	cd ..
	cd client
	mkdir build
	cd build
	cmake ..
	if [ $? -ne 0 ]; then
                echo "Failed to build singlechip sample project"
                exit
        fi
	make
	if [ $? -ne 0 ]; then
                echo "Failed to build singlechip sample project"
                exit
        fi
	
	echo "Build done."
	echo "Application:"
	realpath $SAMPLES_SINGLECHIP/arch/arm/stm32/stm32f746g_disco/client/build/upper*
	echo "Firmware:"
	realpath $SAMPLES_SINGLECHIP/arch/arm/stm32/stm32f746g_disco/server/build/stm32f746g_disco.*
fi  

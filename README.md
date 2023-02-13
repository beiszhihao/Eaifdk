# Embedded AI Framework Development Kit
![Embedded-AI-FDK](https://img.shields.io/github/languages/top/beiszhihao/Eaifdk)
![Embedded-AI-FDK](https://img.shields.io/github/languages/code-size/beiszhihao/Eaifdk)
![Embedded-AI-FDK](https://img.shields.io/github/stars/beiszhihao/Eaifdk?style=social)
![Embedded-AI-FDK](https://img.shields.io/github/forks/beiszhihao/Eaifdk?style=social)
![Embedded-AI-FDK](https://img.shields.io/github/watchers/beiszhihao/Eaifdk?style=social)

![ico](https://user-images.githubusercontent.com/38308279/216873658-bf8235fa-cb24-4b0b-8ed2-35ed573fd148.png)

## About
Embedded AI FDK aims to build target recognition AI solutions for embedded and single-chip devices. We advocate simplification, so that you can build AI programs without AI development experience. You just need to focus on your field and leave the rest to the embedded AI FDK. In addition to simplification, there is also a built-in training framework and reasoning framework. Of course, if we want to use these functions, we need some AI development experience. In order to simplify, we have encapsulated them. Developers only need to know some AI professional languages to use

## Embedded
<img width="900" alt="image" src="https://user-images.githubusercontent.com/38308279/217119386-876bd83f-755e-465d-b737-ba2792d40c12.png">

## Singlechip
![emm](https://user-images.githubusercontent.com/38308279/216880366-cc82fe45-b638-4b0d-b9e5-706ae07756fe.jpg)

## Introduction
This project is mainly an AI ```object recognition``` solution developed for embedded and single-chip devices. You can use this framework to easily train neural network models that can be applied to embedded chips.
At present, Yolo's neural network structure is mainly used in ```object recognition``` in this project. In order to make it run better on embedded chips, its network structure and network model are quantized, and the computing efficiency similar to PC is obtained on the premise of ensuring accuracy

## Embedded computing efficiency (Tensor Flow Lite)
### Hardware Environment
Chip: risc-v (sifive - p550) </br>
Bit: 64 </br>
Frequency: 8.65 GHz </br>
System: Ubuntu 20.04 </br>

### Operational curve
Unit: ms, stable at 7 ms </br>
<img width="460" alt="image" src="https://user-images.githubusercontent.com/38308279/217720175-c164252f-4286-472d-8bd0-ddb50f80a406.png">

### Single-chip computer calculation (cmsis-nn)
### Hardware Environment: </br>
Chip: stm32f746ngh6u (stm32f746g_disco) </br>
Bit: 32 </br>
Frequency: 216 MHz </br>
System: Not </br>

### Operational curve
Unit: ms, stable at 20 ms </br>
<img width="469" alt="image" src="https://user-images.githubusercontent.com/38308279/217721450-8ec4ab46-be0e-4c1a-8918-59f5a3e48359.png">

## Project example
### Object recognition
<img width="311" alt="image" src="https://user-images.githubusercontent.com/38308279/217718218-b25f3b20-6c21-4147-8097-c459c5254b0a.png">

### Eye tracking
<img width="369" alt="image" src="https://user-images.githubusercontent.com/38308279/217719051-b6a5d62e-c992-4629-b4f8-c3735a51cb0c.png">

### Unmanned vehicle
<img width="267" alt="image" src="https://user-images.githubusercontent.com/38308279/217718030-1624fcde-ebe7-431f-99f0-125ada4cb783.png">

## Environment
This project can only be built on Unix-like systems, such as ubuntu, Centos, and Debian OS

## Preparation
The system kit you need to install: </br>
See [package.txt](https://github.com/beiszhihao/Eaifdk/blob/main/script/package.txt) </br> </br>
After the installation of the system kit, you need to install Python dependencies. Use the following command to automatically complete the installation:
```bash
pip3 install -r script/requirements.txt
```

## Build this project
The source code of this project is managed by cmake, which only needs to be compiled according to the construction process of cmake
```
mkdir build
cd build
cmake ..
make
```

## Use it
Before starting, you need to execute the ```setup.sh``` script to complete the setting of environment variables
```
source setup.sh
```

Efdk management tool
```
efdk: Usage: efdk [options] ...

Flags from /home/zhihao/tools/efdk/source/func/main.cpp:
    -anchors (Calculate recommended anchor points for training set) type: bool
      default: false
    -autoLabel (Auto label image) type: string default: ""
    -board (View training panel) type: bool default: false
    -build (Compile model) type: bool default: false
    -map (View average KPI indicators) type: bool default: false
    -path (Specify path) type: string default: ""
    -prefix (File prefix) type: string default: ""
    -reName (Unified image file name, arg:--path --prefix) type: bool
      default: false
    -recall (Calculate recall rate) type: bool default: false
    -samples (Build sample project) type: string default: ""
    -see (View training model) type: bool default: false
    -test (Test result) type: bool default: false
    -train (Start training) type: bool default: false
    -update (Update dataset) type: string default: ""
    -view (View model struct) type: string default: ""
```

## Build samples
### Build embedded projects
```bash
efdk --samples=embedded
```
After building, migrate the ```$EAIFDK_HOME/samples/embedded/server/service.py``` file to the embedded system
Then execute it on the embedded system:
(It is necessary to ensure that ```tflite runtime``` is available on the embedded system)
```bash
python3 service.py
```
If the execution is successful, you will see the following output:
```bash
Start server port: 1200
```

Then enter the application directory:
(Applications support ```windows``` and ```linux```)
```
cd $EAIFDK_HOME/samples/embedded/client
```
Run it:
```bash
npm start
```
If you want to build an application on Windows, you may not be able to use the efdk management tool on Windows. You need to build it manually
```bash
cd $EAIFDK_HOME/samples/embedded/client
npm install
npm start
```

### Build singlechip projects
```bash
efdk --samples=singlechip
```
After successful compilation, the bin file path will be output:
```
Build done.
Application:
/home/eaifdk/samples/singlechip/arch/arm/stm32/stm32f746g_disco/client/build/upper
Firmware:
/home/eaifdk/samples/singlechip/arch/arm/stm32/stm32f746g_disco/server/build/stm32f746g_disco.bin
/home/eaifdk/samples/singlechip/arch/arm/stm32/stm32f746g_disco/server/build/stm32f746g_disco.elf
/home/eaifdk/samples/singlechip/arch/arm/stm32/stm32f746g_disco/server/build/stm32f746g_disco.hex
/home/eaifdk/samples/singlechip/arch/arm/stm32/stm32f746g_disco/server/build/stm32f746g_disco.map
```
Brush the firmware onto the board of the single chip computer. In the example, the openocd configuration file has been provided. You can use this command to directly brush the firmware onto the single chip computer, but only ubuntu is supported:
```bash
cd $EAIFDK_HOME/samples/singlechip/arch/arm/stm32/stm32f746g_disco/server
./openocd/bin/openocd \
-s openocd/boards/arm/stm32f746g_disco/support \
-s openocd/sysroots/x86_64-pokysdk-linux/usr/share/openocd/scripts \
-f openocd/boards/arm/stm32f746g_disco/support/openocd.cfg \
'-c init' \
'-c targets' \
-c 'reset halt' \
-c 'flash write_image erase ./build/stm32f746g_disco.hex' \
-c 'reset halt' \
-c 'verify_image ./build/stm32f746g_disco.hex' \
-c 'reset run' \
-c shutdown
```
## Data set
If you want to update the data set, such as identifying other targets, the framework target recognition uses Mobilenet Yolo v3 neural network, and you need to put your image file into ```$EAIFDK_HOME/dataset/images``` directory, please note that the images directory needs to be cleared first. If you have completed the yolo format marking, you do not need to mark it. If not, you need to use the efdk management tool to mark it first
It should be noted that the image file name needs to be unified before labeling:
(Note that file redefinition only applies to jpg/jpge files)
```bash
efdk --reName --path $EAIFDK_HOME/dataset/images --prefix Face
```
Mark
```bash
efdk --autoLabel=$EAIFDK_HOME/dataset/images
```
Update after marking
```bash
efdk --update=Face
```
The updated parameter is the target class, For example, if your dataset is a dog, then the parameter is a ```dog```

## Train
```bash
efdk --train
```
During training, if you want to view the loss, you can use the board command to create a small server to visualize the training results
```bash
efdk --board
```
You can modify the IP and port in the ```export.sh``` file
```bash
vim $EAIFDK_HOME/script/export.sh
```
Variable:
```bash
BOARD_PORT=8080
LOCAL_IP=127.0.0.1
```
You can see the loss after entering the address in the browser:
<img width="584" alt="image" src="https://user-images.githubusercontent.com/38308279/216920609-7da8f226-3d2d-481a-a26e-f44d22ecec18.png">

## Build model
After training, you should compile them and use the build command
```
efdk --build
```
After construction, ```$EAIFDK_HOME/model``` files of different formats will be generated in the model directory
```
model/face.h5  model/face.pb  model/face.tflite  model/face.weights
```

## View
This project has built-in netron. You can use the view command to start
```
efdk --view $model/face.h5
```
<img width="941" alt="image" src="https://user-images.githubusercontent.com/38308279/217120100-d2971aac-3707-496a-8f20-2e8e13e2d0ff.png">

## Test
The project has built-in TensorFlow reasoning framework, and you can directly use the test:
```
efdk --test
```
<img width="772" alt="image" src="https://user-images.githubusercontent.com/38308279/217120395-7fd39959-db7d-4d61-b3db-f4ac98c82148.png">

# Contributor

For anyone who makes any sharing for this project, we will put him on this list and thank them for everything they have done for this project. Thank you all
|  Name             | Event | Mailbox  |
|  ----            | ----   | ----    |
| Zhou, Zhihao       | Write AI module And Upper computer program , Creator of the project | [Zhihao.Zhou](mailto:zhihao.a.zhou@outlook.com) |

# Feedback
At present, there is only one developer in the project. You can contact the creator directly: [Zhihao.Zhou](mailto:zhihao.a.zhou@outlook.com)

# License

Copyright (c) Zhihao.Zhou Corporation. All rights reserved.

Created by [Zhihao.Zhou]

# Thanks
[AlexeyAB/darknet](https://github.com/AlexeyAB/darknet)

[lutzroeder/netron](https://github.com/lutzroeder/netron)

[dog-qiuqiu/MobileNet-Yolo](https://github.com/dog-qiuqiu/MobileNet-Yolo)

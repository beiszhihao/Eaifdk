#!/usr/bin/env python3
import tensorflow as tf
import cv2
import numpy as np
import socket
import threading
import time
payload_type = {'names': ('cmd', 'end', 'f_size', 't_size'), 'formats': ('u1', 'u1', 'u2', 'u4')}

def xywh2xyxy(x):
    y = np.zeros(x.shape, dtype=np.float32)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y

def non_max_suppression(prediction, conf_thres=0.25):
    x = prediction[prediction[..., 4] > conf_thres]
    if not x.shape[0]:
        return []
    box = xywh2xyxy(x[:, :4])
    return box

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class TfLite:
    def __init__(self, model_content):
        self.interpreter = tf.lite.Interpreter(model_content=model_content)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.dim = (56, 56)
        self.shape = (1280, 720, 3)

    def set_input(self, img, fixed):
        self.dim = tuple(self.input_details[0]['shape'][1:-1])
        input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input = cv2.resize(input, self.dim).astype(np.float32)
        input = input[np.newaxis,:,:,:]
        input = input + fixed
        input = input.astype(np.int8)
        self.interpreter.set_tensor(self.input_details[0]['index'], input)

    def run(self):
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        output = output_data[0].astype(np.float32) 
        return output

    def set_output(self, output, anchors_, parm):
        a, b = parm
        output = (output + a) * b
        nx,ny,_ = output.shape
        anchors = np.zeros([3, 1, 1, 2], dtype=np.float32)
        anchors[0,0,0,:] = [anchors_[0], anchors_[1]]
        anchors[1,0,0,:] = [anchors_[2], anchors_[3]]
        anchors[2,0,0,:] = [anchors_[4], anchors_[5]]
        output = output.reshape((7,7,3,6)).transpose([2,0,1,3])
        yv, xv = np.meshgrid(np.arange(ny), np.arange(nx))
        grid = np.stack((yv, xv), 2).reshape((1, ny, nx, 2)).astype(np.float32)
        output[..., 0:2] = (sigmoid(output[..., 0:2]) + grid) * 8
        output[..., 2:4] = np.exp(output[..., 2:4]) * anchors
        output[..., 4:] = sigmoid(output[..., 4:])
        output = output.reshape((-1, 6))
        boxes = non_max_suppression(output, 0.7)
        ROI = []
        if len(boxes) != 0:
            for detect in boxes:
                detect = detect.astype(np.int32)
                x1 = detect[[0]]
                y1 = detect[[1]]
                x2 = detect[[2]]
                y2 = detect[[3]]
                ROI.append([[x1, y1], [x2, y2]])

        return ROI


class tfThread(threading.Thread):
    SEND_MODEL_CMD = 1
    SEND_INPUT_CMD = 2
    SEND_RUN_CMDS = 3
    GET_RESULT_CMDS = 4
    GET_CPUINFO_CMDS = 5
    SEND_JPG_CMD = 6
    SET_INPUT_PARM = 7
    SET_OUTPUT_PARM = 8
    SNED_ANCHORS = 9

    def __init__(self, threadID, name, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn = conn
        self.tf = None
        self.input = None
        self.roi = []
        self.time = 0
        self.tf_data = [
                {'data': bytes(0), 'status': 0, 'parm': 0},  # output
                {'data': bytes(0), 'status': 0},  # model
                {'data': bytes(0), 'status': 0, 'parm': 0},  # input
        ]
        self.anchors = [0, 0, 0, 0, 0, 0]

    def handler_cmds(self, cmds, conn):
        header = np.frombuffer(cmds[:8], dtype=payload_type)
        header = header.view(np.recarray)[0]
        if header.cmd in (self.SEND_MODEL_CMD, self.SEND_INPUT_CMD, self.SEND_JPG_CMD):
            if header.cmd == self.SEND_JPG_CMD:
                tf_data = self.tf_data[2]
            else:
                tf_data = self.tf_data[header.cmd]
            if tf_data['status'] > 0:
                tf_data['status'] = 0
                tf_data['data'] = bytes(0)
            if header.end == 1:
                tf_data['status'] = 1
            if header.end == 1 and header.cmd == self.SEND_INPUT_CMD:
                tf_data['data'] += cmds[8:8+header.f_size-4]
                shape_data = cmds[8+header.f_size-4: 8+header.f_size]
                self.shape = (int.from_bytes(shape_data[:2], 'little'), int.from_bytes(shape_data[-2:], 'little'), 3)
                self.input = np.frombuffer(tf_data['data'], np.uint8).reshape(self.shape)
            elif header.end == 1 and header.cmd == self.SEND_JPG_CMD:
                tf_data['data'] += cmds[8:8+header.f_size]
                self.input = cv2.imdecode(np.frombuffer(tf_data['data'], np.uint8), cv2.IMREAD_COLOR)
                self.shape = self.input.shape
            else:
                tf_data['data'] += cmds[8:8+header.f_size]
        elif header.cmd == self.SEND_RUN_CMDS:
            if not self.tf or self.tf_data[self.SEND_MODEL_CMD]['status'] != 2:
                self.tf = TfLite(self.tf_data[self.SEND_MODEL_CMD]['data'])
                self.tf_data[self.SEND_MODEL_CMD]['status'] = 2
            self.tf.set_input(self.input, self.tf_data[self.SEND_INPUT_CMD]['parm'])
            start = time.time()
            output = self.tf.run()
            end = time.time()
            self.time = int(1000 * (end - start))
            #print(1000 * (end - start))
            self.roi = self.tf.set_output(output, self.anchors, self.tf_data[0]['parm'])
        elif header.cmd == self.GET_RESULT_CMDS:
            send_data = bytes(0)
            header = np.zeros(1, dtype=payload_type)
            header = header.view(np.recarray)[0]
            header.cmd = self.GET_RESULT_CMDS
            for val in self.roi:
                # x1, y1 = val[0] * np.array(self.shape[:-1]) / np.array(self.tf.dim)
                # x2, y2 = val[1] * np.array(self.shape[:-1]) / np.array(self.tf.dim)
                # data = np.array([x1, y1, x2, y2])
                # data[::2] = np.clip(data[::2], 0, self.shape[0])
                # data[1::2] = np.clip(data[1::2], 0, self.shape[1])
                x1, y1 = val[0]
                x2, y2 = val[1]
                data = np.array([x1, y1, x2, y2])
                data = np.clip(data, 0, 56)
                data = data.astype('u2')
                roidata = "roi:["
                roidata += '{},'.format(data[0])
                roidata += '{},'.format(data[1])
                roidata += '{},'.format(data[2])
                roidata += '{},'.format(data[3])
                roidata += '{}'.format(self.time)
                roidata += ']'
                # send_data += data.tobytes()
                send_data += roidata.encode()

            header.t_size = len(send_data)
            header.f_size = self.time
            conn.send(header.tobytes() + send_data + bytes(1024 - header.itemsize - len(send_data)))
        elif header.cmd == self.SET_INPUT_PARM:
            self.tf_data[self.SEND_INPUT_CMD]['parm'] = eval(cmds[8:8+header.f_size])
        elif header.cmd == self.SET_OUTPUT_PARM:
            r_data = cmds[8: 8+header.f_size]
            a, b = r_data.decode().split('\n')
            self.tf_data[0]['parm'] = (eval(a), eval(b))
        elif header.cmd == self.SNED_ANCHORS:
            self.anchors = eval(cmds[8:8+header.f_size])
        elif header.cmd == self.GET_CPUINFO_CMDS:
            header = np.zeros(1, dtype=payload_type)
            header = header.view(np.recarray)[0]
            header.cmd = self.GET_CPUINFO_CMDS
            cpuinfo = '11th Gen Intel(R) Core(TM) i9-11900K @ 3.50GHz'
            cpuinfo += '\n'
            cpuinfo += '16'
            send_cpu = 'cpui['
            send_cpu += cpuinfo
            send_cpu += ']'
            data = send_cpu.encode()
            header.f_size = len(data)
            conn.send(header.tobytes() + data + bytes(1024 - header.itemsize - len(data)))

    def run(self):
        print(f"Connect from: {self.name}")
        data = bytes(0)
        while True:
            data += conn.recv(1024)
            if len(data) == 0:
                break
            if len(data) >= 1024:
                self.handler_cmds(data[:1024], conn)
                data = data[1024:]
        print(f"{self.name} disconnected.")


if __name__ == '__main__':
    s = socket.socket()
    s.bind(('0.0.0.0', 1200))
    s.listen(1)
    print('Start server port: 1200')
    try:
        while True:
            conn, addr = s.accept()
            tfp = tfThread(1, f'{addr[0]}:{addr[1]}', conn)
            tfp.start()
    except KeyboardInterrupt:
        s.close()

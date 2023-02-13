import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend as K
import cv2
import numpy as np

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

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return [x, y, w, h]

model = load_model(sys.argv[1], compile=False)
#plot_model(model, to_file='model.png', show_shapes=True)
img = cv2.imread(sys.argv[2])
input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

H, W, _ = img.shape
w_scale = W/56.
h_scale = H/56.
input = cv2.resize(input, (56, 56))
input = input[np.newaxis,:,:,:]
input = input/255.

output = model(input)
output = output.numpy()[0]
nx,ny,_ = output.shape
anchors = np.zeros([3, 1, 1, 2], dtype=np.float32)
anchors[0,0,0,:] = [9, 14]
anchors[1,0,0,:] = [12, 17]
anchors[2,0,0,:] = [22, 21]
output = output.reshape((7,7,3,6)).transpose([2,0,1,3])
yv, xv = np.meshgrid(np.arange(ny), np.arange(nx))
grid = np.stack((yv, xv), 2).reshape((1, ny, nx, 2)).astype(np.float32)
output[..., 0:2] = (sigmoid(output[..., 0:2]) + grid) * 8
output[..., 2:4] = np.exp(output[..., 2:4]) * anchors
output[..., 4:] = sigmoid(output[..., 4:])
output = output.reshape((-1, 6))
boxes = non_max_suppression(output, 0.7)

if len(boxes) != 0:
    path = os.path.dirname(os.path.abspath(sys.argv[2]))
    name = os.path.basename(sys.argv[2])
    name = os.path.splitext(name)[0]
    file = open(path + '/' + name + ".txt",'w')
    for detect in boxes:
        detect[[0,2]] *= w_scale
        detect[[1,3]] *= h_scale
        detect = detect.astype(np.int32)
        x,y,w,h = convert((W, H),(detect[[0]], detect[[2]], detect[1], detect[3]))
        write = '0 ' + str(x).strip('[]') + ' ' + str(y).strip('[]') + ' ' + str(w).strip('[]') + ' ' + str(h).strip('[]')
        file.write(write)

import torch
import numpy as np
import torch.nn as nn
from torch.autograd import Variable

from modules.stn_invert import STNInvert
from modules.gridgen import AffineGridGen, CylinderGridGen, CylinderGridGenV2, DenseAffine3DGridGen, DenseAffine3DGridGen_rotate

nframes = 12
height = 64
width = 128
channels = 3

inputImages = torch.randn(nframes, height, width, channels)
grids = torch.zeros(nframes, height, width, 2)

input1, input2 = Variable(inputImages, requires_grad=True), Variable(grids, requires_grad=True)
input1.data.uniform_()
input2.data.uniform_(-1,1)

input = Variable(torch.from_numpy(np.array([[[1, 0, 0.1], [0, 1, 0]]], dtype=np.float32)), requires_grad = True)

g = AffineGridGen(64, 128, aux_loss = True)
out, aux = g(input)
print out.size()
out.backward(out.data)

print input2.size()
s = STNInvert()
out = s(input1, input2)
print(out.size())
out.backward(input1.data)
print(input1.grad.size())


#input1, input2 = Variable(inputImages.cuda(0), requires_grad=True), Variable(grids.cuda(0), requires_grad=True)
#input1.data.uniform_()
#input2.data.uniform_(-1,1)

with torch.cuda.device(0):
    s = STNInvert()
    input1 = input1.cuda()
    input2 = input2.cuda()
    out = s(input1, input2)
    print('cuda',out.size())
    out.backward(input1.data)
    print('done')

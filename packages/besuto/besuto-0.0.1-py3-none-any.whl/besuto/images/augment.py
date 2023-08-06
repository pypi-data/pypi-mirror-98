import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image

def augment(array,generation,size=(256,256)):
  #lightlevel augmentation
  HFR,LLR,RRR,result = list(),list(),list(),list()
  hflip = np.expand_dims(array,0)
  hfgen = ImageDataGenerator(horizontal_flip=True)
  hfgenerate = hfgen.flow(hflip,batch_size=1)
  for i in range(generation):
    batch = hfgenerate.next()
    image = batch[0].astype('uint8')
    HFR.append(image)
  for j in HFR:
    Llevel = np.expand_dims(j,0)
    LLgen = ImageDataGenerator(brightness_range=[0.2,1.0])
    LLgenerate = LLgen.flow(Llevel,batch_size=1)
    for x in range(generation):
      batch = LLgenerate.next()
      image = batch[0].astype('uint8')
      LLR.append(image)
  for k in LLR:
    RRotage = np.expand_dims(k,0)
    RRgen = ImageDataGenerator(rotation_range = 53)
    RRgenerate = RRgen.flow(RRotage,batch_size=1)
    for y in range(generation):
      batch = RRgenerate.next()
      image = batch[0].astype('uint8')
      RRR.append(image)
  for z in RRR:
    image = Image.fromarray(z)
    image = image.resize(size)
    result.append(np.asarray(image))
  return np.asarray(result)

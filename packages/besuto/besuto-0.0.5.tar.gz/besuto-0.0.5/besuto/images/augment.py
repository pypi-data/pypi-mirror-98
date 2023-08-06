import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from numpy import asarray
from mtcnn import MTCNN
import os
import pandas as pd
import logging
from tqdm import tqdm


def extract_face(filename, required_size=(256,256)):
  image = Image.open(filename)
  image = image.convert('RGB')
  array = asarray(image)
  detector = MTCNN()
  face_detected = detector.detect_faces(array)
  if face_detected ==[]:
    return []
  x1, y1, width, height = face_detected[0]['box']
  x1, y1 = abs(x1), abs(y1)
  x2, y2 = x1 + width, y1 + height
  face = array[y1:y2, x1:x2]
  image = Image.fromarray(face)
  image = image.resize(required_size)
  face_array = asarray(image)
  return face_array

def folder_extract_face(directory):
  faces =list()
  for filename in tqdm(os.listdir(directory)):
    path = directory+ filename
    face = extract_face(path)
    if face != []:
      faces.append(face)
    else:
      pass
  return asarray(faces)

def test(directory ='',aug=True):
  os.listdir(directory)

def multifolder_folder_extract_face(directory ='',aug=True,gen=5):
  X,y = list(),list()
  # loop every folder
  print('searching files in {}'.format(directory))
  for folder in tqdm(sorted(os.listdir(directory))):
    path = directory + folder+'/'
    if not os.path.isdir(path):
      continue
    print('loading {} faces...'.format(folder))
    faces = folder_extract_face(path)
    augmentL = list()
    if aug == True:
      for i in faces:
        print('Augmenting {} faces...'.format(folder))
        augmentL.extend(Augment(i,generation=gen))
    else:
      augmentL.extend(faces)
    labels = [folder for i in range(len(augmentL))]
    X.extend(augmentL)
    y.extend(labels)
  return asarray(X), asarray(y)

def convertOHC(label):
  category = np.array(label.unique())
  n_categories = len(category)
  ohe_labels = np.zeros((len(label), n_categories))
  for ii in range(len(label)):
    # Find the location of this label in the categories variable
    jj = np.where(category == label[ii])
    # Set the corresponding zero to one
    ohe_labels[ii,jj] = 1
  return ohe_labels

def labelEncode(label):
  data = pd.DataFrame({"label":label})
  category = np.array(data['label'].unique())
  n_categories = len(category)
  ohe_labels = convertOHC(data['label'])
  data['encode'] = [i for i in ohe_labels]
  data['cnn_output_class'] = [np.argmax(i) for i in data['encode']]
  return ohe_labels,n_categories,data

def load_face_dataset(directory='',aug=True):
  X,y = multifolder_folder_extract_face(directory,aug=aug)
  y,num_class,data = labelEncode(y)
  #show result of one hot code
  print('_'*100)
  print("feature shape : ",X.shape)
  print("label shape   : ",y.shape)
  return X,y,num_class,data

def Augment(array,generation,size=(256,256)):
  #lightlevel augmentation
  logging.getLogger('tensorflow').setLevel(logging.FATAL)
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

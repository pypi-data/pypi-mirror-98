from augment import augment
from PIL import Image
from numpy import asarray
from mtcnn import MTCNN
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

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

def input_extract_face(directory):
  faces =list()
  for filename in os.listdir(directory):
    path = directory+ filename
    face = extract_face(path)
    if face != []:
      faces.append(face)
    else:
      pass
  return asarray(faces)

def load_dataset_multifolder(directory ='',aug=True):
  X,y = list(),list()
  # loop every folder
  for folder in sorted(os.listdir(directory)):
    path = directory + folder+'/'
    if not os.path.isdir(path):
      continue
    faces = input_extract_face(path)
    augment = list()
    if aug == True:
      for i in faces:
        augment.extend(Augment(i,generation=5))
    else:
      augment.extend(faces)
    labels = [folder for i in range(len(augment))]
    X.extend(augment)
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

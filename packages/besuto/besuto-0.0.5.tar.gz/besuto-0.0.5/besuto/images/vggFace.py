from keras_vggface.vggface import VGGFace
from keras.models import Model, load_model
from keras.layers import Dense,Flatten
from keras.callbacks import ModelCheckpoint , EarlyStopping
from tqdm import tqdm
from timeit import default_timer as timer

class modelvggface():
    def __init__(self,models= ['vgg16','resnet50','senet50'],input_shape = (256,256,3),num_class=0,X=None,y=None,name=""):
        #all achitect avaliable ['vgg16','resnet50','senet50']
        self.input_shape = input_shape
        self.num_class = num_class
        self.X = X
        self.y = y
        self.models = models = [{'name':i+name,'model':self.getVggFacemodel(architect=i)}for i in tqdm(models)]
        
    
    def getVggFacemodel(self,architect=''):
        model = VGGFace(model=architect,weights ='vggface',include_top =False,input_shape = self.input_shape)
        for layer in model.layers:
            layer.trainable = False
        if architect == 'vgg16':
            top = model.get_layer('pool5').output
        else:
            top = model.get_layer('avg_pool').output
        top = Flatten(name='flatten')(top)
        top = Dense(1024,activation='relu')(top)
        top = Dense(1024,activation='relu')(top)
        top = Dense(512,activation='relu')(top)
        output = Dense(self.num_class,activation='softmax')(top)
        Result = Model(inputs=model.input,outputs=output)
        return Result
    
    def trains(self):
        output = {}
        '''if self.X == None or self.y == None:
            raise Exception('there are missing feature or label that require for training')'''
        for model in self.models:
            Model = model['model']
            checkpoint = ModelCheckpoint('/content/drive/My Drive/Colab Notebooks/facelink/model output/'+model['name']+'.h5',monitor='val_loss',mode='min',save_best_only=True,verbose=1)
            earlystop = EarlyStopping(patience=3,monitor='val_loss',verbose=1)
            Model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
            start = timer()
            h = Model.fit(self.X,self.y,epochs=100,callbacks=[earlystop,checkpoint],validation_split=0.2)
            end = timer()
            traintime = end-start
            output[model['name']] = {
                    'history':h,
                    'model':Model,
                    'time':traintime
            }
        return output
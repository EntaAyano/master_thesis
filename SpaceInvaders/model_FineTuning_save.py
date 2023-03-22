from keras.preprocessing.image import ImageDataGenerator
from keras.applications.resnet50 import ResNet50
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout
#from tensorflow.keras.optimizers import SGD
#from tensorflow.keras.optimizers import Adam
#from keras.optimizers import adam
from keras.optimizers import SGD
from tensorflow.python.keras.models import load_model
import pandas as pd

classes = ["A-B","A-S","Agent","Invader_singular","S-I_p","A-B-S","A-S-I_p","B-S","Invader_plural","SafeArea","B-I_p"]
nb_classes = len(classes)
train_data_dir = './dataset/dataset3/train'
validation_data_dir = './dataset/dataset3/val'
nb_train_samples = 3145
nb_validation_samples = 446
img_width, img_height = 50, 50

train_datagen = ImageDataGenerator(rescale=1.0 / 255, zoom_range=0.2, horizontal_flip=True)
validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=16)

validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=16)

input_tensor = Input(shape=(img_width, img_height, 3))
ResNet50 = ResNet50(include_top=False, weights='imagenet',input_tensor=input_tensor)

top_model = Sequential()
top_model.add(Flatten(input_shape=ResNet50.output_shape[1:]))
top_model.add(Dense(nb_classes, activation='softmax'))

model = Model(input=ResNet50.input, output=top_model(ResNet50.output))

#model = load_model("model_FineTuning-2.h5")

model.compile(loss='categorical_crossentropy',
        optimizer=SGD(lr=1e-3, momentum=0.9),
        #optimizer=adam(lr=1e-3, decay=1e-6),
        metrics=['accuracy'])

history = model.fit_generator(
        train_generator,
        #samples_per_epoch=nb_train_samples,
        steps_per_epoch = nb_train_samples,
        #nb_epoch=1,
        epochs = 10,
        validation_data=validation_generator,
        #nb_val_samples=nb_validation_samples)
        validation_steps=nb_validation_samples)

model.save("model_FineTuning-4.h5")

hist_df = pd.DataFrame(history.history)
hist_df.to_csv('history_4.csv')

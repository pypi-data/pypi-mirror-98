import os
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np


class CNN:
  pass

cnn = CNN()

def init(class_count=2):
  
  cnn.class_count = class_count

  cnn.model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    # tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(cnn.class_count, activation='sigmoid')
  ])

  cnn.model.compile(optimizer=RMSprop(lr=0.001),
              loss='categorical_crossentropy',
              metrics = ['accuracy'])

  print('딥러닝 모델 설정이 완료되었습니다.')

def train(train_dir, repeat=5):

  cnn.categories = os.listdir( train_dir )

  train_datagen = ImageDataGenerator( rescale = 1.0/255. )
  
  train_generator = train_datagen.flow_from_directory(train_dir,
                                                    batch_size=20,
                                                    class_mode='categorical',
                                                    target_size=(150, 150))
  history = cnn.model.fit(train_generator,
                    steps_per_epoch=100,
                    epochs=repeat,
                    verbose=2)

  return history

def predict(target_path):
  img=image.load_img(target_path , target_size=(150, 150))
  x=image.img_to_array(img)
  x=np.expand_dims(x, axis=0)
  images = np.vstack([x])
  classes = cnn.model.predict(images, batch_size=1)
  index = np.argmax(classes[0])
  return cnn.categories[index]
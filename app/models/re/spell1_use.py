import tensorflow as tf
import os
import numpy as np

# Load data
data_dir = "D:/PycharmProjects/TeamProject/app/models/data/frames"
label_path = "D:/PycharmProjects/TeamProject/app/models/label/spell1_use_gt.txt"

# Create a list of image file paths and labels
image_paths = []
labels = []
with open(label_path, 'r') as f:
    for line in f:
        image_file, label = line.strip().split(',')
        image_paths.append(os.path.join(data_dir, image_file))
        labels.append(label.strip())

num_classes = 2
label_map = {'0': 0, '1': 1}
labels = [label_map[label] for label in labels]
labels = tf.keras.utils.to_categorical(labels, num_classes)

# Define function to preprocess images
def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.crop_to_bounding_box(image, 148, 610, 22, 22)
    image = tf.image.resize(image, [224, 224])
    image /= 255.0  # normalize pixel values to [0,1]
    return image

# Define function to load and preprocess image file
def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)

# Create TensorFlow Dataset
dataset = tf.data.Dataset.from_tensor_slices((image_paths[:1154], labels[:1154]))
dataset = dataset.map(lambda path, label: (load_and_preprocess_image(path), label))
dataset = dataset.shuffle(len(image_paths))

# Define model
num_classes = 2
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, 3, activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(dataset.batch(32), epochs=10)

model_save_path = "D:/PycharmProjects/TeamProject/app/models/model_save/spell1_use_epochs10.h5"
model.save(model_save_path)
'''
C:\ProgramData\Anaconda3\python.exe D:\PycharmProjects\TeamProject\app\models\re\spell1_use.py 
2023-03-22 18:10:59.416061: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX AVX2
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
WARNING:tensorflow:From C:\Users\AiA\AppData\Roaming\Python\Python39\site-packages\tensorflow\python\autograph\pyct\static_analysis\liveness.py:83: Analyzer.lamba_check (from tensorflow.python.autograph.pyct.static_analysis.liveness) is deprecated and will be removed after 2023-09-23.
Instructions for updating:
Lambda fuctions will be no more assumed to be used in the statement where they are used, or at least in the same block. https://github.com/tensorflow/tensorflow/issues/56089
Epoch 1/10
37/37 [==============================] - 13s 294ms/step - loss: 0.6175 - accuracy: 0.6612
Epoch 2/10
37/37 [==============================] - 12s 296ms/step - loss: 0.4952 - accuracy: 0.7426
Epoch 3/10
37/37 [==============================] - 12s 297ms/step - loss: 0.4549 - accuracy: 0.7773
Epoch 4/10
37/37 [==============================] - 12s 298ms/step - loss: 0.4153 - accuracy: 0.8111
Epoch 5/10
37/37 [==============================] - 12s 302ms/step - loss: 0.3570 - accuracy: 0.8423
Epoch 6/10
37/37 [==============================] - 12s 300ms/step - loss: 0.3202 - accuracy: 0.8640
Epoch 7/10
37/37 [==============================] - 13s 305ms/step - loss: 0.3242 - accuracy: 0.8596
Epoch 8/10
37/37 [==============================] - 13s 305ms/step - loss: 0.3028 - accuracy: 0.8666
Epoch 9/10
37/37 [==============================] - 12s 300ms/step - loss: 0.2799 - accuracy: 0.8847
Epoch 10/10
37/37 [==============================] - 12s 301ms/step - loss: 0.2606 - accuracy: 0.8891

Process finished with exit code 0
'''
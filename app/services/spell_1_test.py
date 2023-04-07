import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img
import numpy as np
import os

# Load the saved model
model_path = 'C:/Users/AiA/Desktop/TeamProject/app/models/model_save/spell1_use_epochs10.h5'
model = keras.models.load_model(model_path)

# Define the image size for the model
img_size = (224, 224)

# Define the path to the directory containing the test images
test_dir = 'C:/Users/AiA/Desktop/TeamProject/app/services/testdata'

# Loop through each image in the directory and test the model
for filename in os.listdir(test_dir):
    # Load the image and resize it to the appropriate size
    img = load_img(os.path.join(test_dir, filename), target_size=img_size)
    # Convert the image to a numpy array
    img_array = img_to_array(img)
    # Reshape the array to match the input shape of the model
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize the image data
    img_array = keras.applications.mobilenet_v2.preprocess_input(img_array)
    # Use the model to make a prediction on the image
    prediction = model.predict(img_array)
    # Print the prediction for the image
    print(prediction)
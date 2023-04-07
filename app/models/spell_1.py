import cv2
import tensorflow as tf
import numpy as np
import os

# Set paths to data and labels
data_path = 'D:/PycharmProjects/TeamProject/app/models/data/3frame_videos_but_348_480p'
label_path = './label/spell_1_truth.txt'

# Define hyperparameters
num_classes = 5
batch_size = 16
epochs = 7
learning_rate = 0.001

# Define a function to extract frames from videos
def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (224, 224))
            frame = tf.keras.preprocessing.image.img_to_array(frame)
            frames.append(frame)
        else:
            break
    cap.release()
    return np.array(frames)

# Load data and labels
# Load data and labels
def load_data(data_path, label_path, max_frames=47):
    with open(label_path, 'r') as f:
        labels = f.readline().split(',')
        labels = [int(label)-1 for label in labels]
    data = []
    for filename in os.listdir(data_path):
        video_path = os.path.join(data_path, filename)
        frames = extract_frames(video_path)
        if frames.shape[0] > max_frames:
            frames = frames[:max_frames]  # Truncate frames
        else:
            pad_width = ((0, max_frames - frames.shape[0]), (0, 0), (0, 0), (0, 0))
            frames = np.pad(frames, pad_width, 'constant')  # Pad frames
        frames_tensor = tf.convert_to_tensor(frames)  # Convert frames to tensor
        data.append(frames_tensor)
    return tf.stack(data), np.array(labels)  # Stack the tensors to create a batch

x_train, y_train = load_data(data_path, label_path)

# Split data into training and validation sets
num_samples = len(x_train)
num_train_samples = int(num_samples * 0.8)
train_indices = tf.constant(np.random.choice(num_samples, num_train_samples, replace=False))
val_indices = tf.constant(np.setdiff1d(np.arange(num_samples), train_indices))
x_val, y_val = tf.gather(x_train, val_indices), tf.gather(y_train, val_indices)
x_train, y_train = tf.gather(x_train, train_indices), tf.gather(y_train, train_indices)

# Define model architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv3D(16, (3, 3, 3), activation='relu', input_shape=(47, 224, 224, 3)),
    tf.keras.layers.MaxPooling3D((2, 2, 2)),
    tf.keras.layers.Conv3D(32, (3, 3, 3), activation='relu'),
    tf.keras.layers.MaxPooling3D((2, 2, 2)),
    tf.keras.layers.Conv3D(64, (3, 3, 3), activation='relu'),
    tf.keras.layers.MaxPooling3D((2, 2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train model
model.fit(x_train, y_train,
          validation_data=(x_val, y_val),
          batch_size=batch_size,
          epochs=epochs)

# Save model
model.save('D:/PycharmProjects/TeamProject/app/models/model_save/spell_1.h5')
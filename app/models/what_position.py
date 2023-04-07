import cv2
import tensorflow as tf
import numpy as np
import os

# Set paths to data and labels
data_path = 'D:/PycharmProjects/TeamProject/app/models/data/3frame_videos_but_200'
label_path = './label/what_position.txt'

# Define hyperparameters
num_classes = 5
batch_size = 16
epochs = 10
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


# Define a generator function to load data in batches
def data_generator(data_path, label_path, batch_size, max_frames=47):
    with open(label_path, 'r') as f:
        labels = f.readlines()
        labels = [x.strip() for x in labels]
        labels = labels[:200]
        for i in range(len(labels)):
            if labels[i] == 'top':
                labels[i] = 0
            elif labels[i] == 'jungle':
                labels[i] = 1
            elif labels[i] == 'mid':
                labels[i] = 2
            elif labels[i] == 'ad carry':
                labels[i] = 3
            elif labels[i] == 'support':
                labels[i] = 4
    while True:
        data = []
        for filename in np.random.permutation(os.listdir(data_path)):
            video_path = os.path.join(data_path, filename)
            frames = extract_frames(video_path)
            if frames.shape[0] > max_frames:
                frames = frames[:max_frames]  # Truncate frames
            else:
                pad_width = ((0, max_frames - frames.shape[0]), (0, 0), (0, 0), (0, 0))
                frames = np.pad(frames, pad_width, 'constant')  # Pad frames
            frames_tensor = tf.convert_to_tensor(frames)  # Convert frames to tensor
            data.append(frames_tensor)
            if len(data) == batch_size:
                yield tf.stack(data), np.array(labels)[:batch_size]  # Stack the tensors to create a batch
                data = []


# Split data into training and validation sets
num_samples = len(os.listdir(data_path))
num_train_samples = int(num_samples * 0.8)
train_data = data_generator(data_path, label_path, batch_size, max_frames=47)
val_data = data_generator(data_path, label_path, batch_size, max_frames=47)

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
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train model
model.fit(train_data,
          steps_per_epoch=num_train_samples // batch_size,
          validation_data=val_data,
          validation_steps=(num_samples - num_train_samples) // batch_size,
          epochs=epochs)

model.save('D:/PycharmProjects/TeamProject/app/models/model_save/what_position.h5')
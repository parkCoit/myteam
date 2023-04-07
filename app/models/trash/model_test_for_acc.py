import torch
import torchvision

from app.models.trash.spell_1 import VideoClassifier

# Define the class names
class_names = ['없음', '있음', '중간에 사용', '없다 생김', '없다 생긴걸 사용']

# Load the model
model_state_dict = torch.load('../model_save/trash/video_classifier.pth')
model = VideoClassifier()
model.load_state_dict(model_state_dict)
model.eval()

# Load the video and make predictions
video_path = r'/app/models/data/test/13-1_KR-6333959106_03.webm'
video, _, _ = torchvision.io.read_video(video_path, pts_unit='sec')
video = video.permute(3, 0, 1, 2)  # Reshape to (num_channels, num_frames, height, width)
with torch.no_grad():
    outputs = model(video)
predicted_class = torch.argmax(outputs).item()

# Print the prediction
print(f'Predicted class: {class_names[predicted_class]}')
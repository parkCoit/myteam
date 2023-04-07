ls = []
ls2 = []
import os

# Define the directory path
dir_path = "D:/PycharmProjects/TeamProject/app/models/data/frames"

# Initialize a count variable to keep track of the number of image files
count = 0

# Loop through all files in the directory
for file_name in os.listdir(dir_path):

    # Check if the file is an image file
    if file_name.endswith(".jpg") or file_name.endswith(".png"):

        # Increment the count variable
        count += 1

        # Print the file name if the count is less than or equal to 1154
        if count <= 1154:
            ls.append(file_name)

        # Break out of the loop if the count reaches 1154
        if count == 1154:
            break
for i in range(0,329):
    ls2.append(1)
for i in range(329,558):
    ls2.append(0)
for i in range(0,467):
    ls2.append(1)
for i in range(467,596):
    ls2.append(0)
print(len(ls))
print(len(ls2))
for i in range (1154):
    print(f"{ls[i]},{ls2[i]}")
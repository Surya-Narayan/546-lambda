from boto3 import client as boto3_client
import face_recognition
import pickle
import cv2
import numpy as np
import os

input_bucket = "546proj2"
output_bucket = "546proj2output"

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):
	video_file_path = "test_cases/test_case_1/test_1.mp4"
	output_path = "output/"
	# Load the known face encodings and names from files

	encodings_dict = open_encoding("encoding")

	# Convert the dictionary to separate lists of known_faces and known_names

	known_faces = list(encodings_dict['encoding'])
	known_names = list(encodings_dict['name'])

	# print(known_faces)
	print(type(known_names))

	# Extract frames from the video using ffmpeg
	os.system(f"ffmpeg -i {video_file_path} -r 1 {output_path}image-%3d.jpeg")

	# Process each extracted frame
	for i in range(1, 100):  # Adjust the range depending on the number of frames extracted
		image_path = f"{output_path}image-{i:03d}.jpeg"

		if os.path.isfile(image_path):
			# Load the image
			unknown_image = face_recognition.load_image_file(image_path)
			face_encodings = face_recognition.face_encodings(unknown_image)[0]
			matches = face_recognition.compare_faces(known_faces, face_encodings)
			print(matches)
			name = "Unknown"

			# If there is a match, use the known face's name
			if True in matches:
				first_match_index = matches.index(True)
				name = known_names[first_match_index]
				print(name)

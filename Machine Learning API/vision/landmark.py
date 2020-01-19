import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def detect_landmarks(path):
    """Detects landmarks in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude',lat_lng.latitude)
            print('Longitude',lat_lng.longitude)

detect_landmarks('landmark.jpg')
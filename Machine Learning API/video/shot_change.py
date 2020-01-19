import sys
import time

from google.cloud import videointelligence_v1beta2
from google.cloud.videointelligence_v1beta2 import enums

def analyze_shots(path):
    """ Detects camera shot changes. """
    video_client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
    features = [enums.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for shot change annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    shots = operation.result().annotation_results[0].shot_annotations

    for i, shot in enumerate(shots):
        start_time = (shot.start_time_offset.seconds +
                      shot.start_time_offset.nanos / 1e9)
        end_time = (shot.end_time_offset.seconds +
                    shot.end_time_offset.nanos / 1e9)
        print('\tShot {}: {} to {}'.format(i, start_time, end_time))

analyze_shots('gs://demomaker/volleyball.mp4')
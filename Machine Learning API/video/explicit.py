import sys
import time

from google.cloud import videointelligence_v1beta2
from google.cloud.videointelligence_v1beta2 import enums

def analyze_explicit_content(path):
    """ Detects explicit content from the GCS path to a video. """
    video_client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
    features = [enums.Feature.EXPLICIT_CONTENT_DETECTION]

    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for explicit content annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    explicit_annotation = (operation.result().annotation_results[0].
                           explicit_annotation)

    likely_string = ("Unknown", "Very unlikely", "Unlikely", "Possible",
                     "Likely", "Very likely")

    for frame in explicit_annotation.frames:
        frame_time = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        print('Time: {}s'.format(frame_time))
        print('\tpornography: {}'.format(
            likely_string[frame.pornography_likelihood]))

analyze_explicit_content('gs://demomaker/cat.mp4')
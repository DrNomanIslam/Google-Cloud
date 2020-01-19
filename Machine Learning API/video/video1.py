import sys
import time
import os

from google.cloud import videointelligence_v1beta2
from google.cloud.videointelligence_v1beta2 import enums

video_client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
features = [enums.Feature.LABEL_DETECTION]

operation = video_client.annotate_video('gs://demomaker/volleyball.mp4', features)
print('\nProcessing video for label annotations:')

while not operation.done():
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(15)

print('\nFinished processing.')

# first result is retrieved because a single video was processed
results = operation.result().annotation_results[0]

for i, segment_label in enumerate(results.segment_label_annotations):
    print('Video label description: {}'.format(
        segment_label.entity.description))
    for category_entity in segment_label.category_entities:
        print('\tLabel category description: {}'.format(
            category_entity.description))

    for i, segment in enumerate(segment_label.segments):
        start_time = (segment.segment.start_time_offset.seconds +
                      segment.segment.start_time_offset.nanos / 1e9)
        end_time = (segment.segment.end_time_offset.seconds +
                    segment.segment.end_time_offset.nanos / 1e9)
        positions = '{}s to {}s'.format(start_time, end_time)
        confidence = segment.confidence
        print('\tSegment {}: {}'.format(i, positions))
        print('\tConfidence: {}'.format(confidence))
    print('\n')
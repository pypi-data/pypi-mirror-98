#!/usr/bin/python3

import argparse
import tator
from collections import defaultdict
from dateutil.parser import parse
import os
from pprint import pprint
import datetime
import tqdm
import traceback

if __name__=="__main__":
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--host', type=str,default='https://www.tatorapp.com')
  parser.add_argument('--token', type=str,required=True)
  parser.add_argument('--trip-id', required=True)
  parser.add_argument('--type-id', required=True)
  parser.add_argument('--gap-tolerance', default=240, type=int)
  args = parser.parse_args()

  api = tator.get_api(args.host, args.token)

  media_type = api.get_media_type(args.type_id)
  project = media_type.project

  media_list = api.get_media_list(project,
                                  type=args.type_id,
                                  search=f"Trip:\"{args.trip_id}\"")

  by_camera=defaultdict(lambda:[])
  print(f"Processing {len(media_list)} media files")
  for media in tqdm.tqdm(media_list):
    length = media.num_frames / media.fps
    camera = media.attributes.get('Camera','Unknown')
    by_camera[camera].append(media)

  gaps=defaultdict(lambda:dict())
  print("Gap Analysis")
  for camera,medias in by_camera.items():
    medias.sort(key= lambda x: x.name)
    for idx,media in enumerate(medias):
      if idx != 0:
        camera = media.attributes.get('Camera', 'Unknown')
        last = medias[idx-1]
        end_name = last.name
        end_start_time = os.path.splitext(end_name)[0].replace('_',':')
        end_start_time = parse(end_start_time)
        end_length = datetime.timedelta(seconds=last.num_frames/last.fps)
        end_end_time = end_start_time + end_length
        this_start_time = os.path.splitext(media.name)[0].replace('_',':')
        this_start_time = parse(this_start_time)
        delta = this_start_time - end_end_time
        if delta > datetime.timedelta(seconds=args.gap_tolerance):
          gaps[end_start_time][camera] = (end_end_time,delta)

  for time,gap in gaps.items():
    print(f"Gap in {time}")
    for camera,info in gap.items():
      print(f"\t{camera}\t{info[0]}\t{info[1]}")
        
      
  

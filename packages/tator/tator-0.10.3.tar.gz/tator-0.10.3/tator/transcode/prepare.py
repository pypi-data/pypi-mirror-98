#!/usr/bin/env python

""" Prepares media for transcode."""

import argparse
import os
import sys
import json
import subprocess
import logging
from urllib.parse import urlparse

from progressbar import progressbar

from ..util import md5sum

from .create_media import create_media
from .determine_transcode import determine_transcode
from .make_thumbnails import make_thumbnails

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Full transcode pipeline on a directory of files.')
    parser.add_argument('--url', type=str, help='URL where original file is hosted.')
    parser.add_argument('--work_dir', type=str, help='Directory where info should be saved.')
    parser.add_argument('--host', type=str, default='https://www.tatorapp.com', help='Host URL.')
    parser.add_argument('--token', type=str, help='REST API token.')
    parser.add_argument('--project', type=int, help='Unique integer specifying project ID.')
    parser.add_argument('--type', type=int, help='Unique integer specifying a media type.')
    parser.add_argument('--name', type=str, help='Name of the media.')
    parser.add_argument('--section', type=str, help='Media section name.')
    parser.add_argument('--attributes', type=str, help="Attributes for media")
    parser.add_argument('--media_id', type=int, help="Existing media ID, if applicable",
                        default=-1)
    parser.add_argument('--gid', type=str, help="Upload group ID.")
    parser.add_argument('--uid', type=str, help="Upload unique ID.")
    parser.add_argument('--group_to', type=int, default=480,
                         help='Vertical resolutions below this will be transcoded with '
                              'multi-headed ffmpeg.')
    parser.add_argument('--size', type=int, help="Size in bytes of the uploaded file.")
    return parser.parse_args()

def get_file_paths(url, work_dir):
    name = os.path.basename(urlparse(url).path)
    paths = {
        'original': os.path.join(work_dir, name),
        'thumbnail': os.path.join(work_dir, 'thumbnail.jpg'),
        'thumbnail_gif': os.path.join(work_dir, 'thumbnail_gif.gif'),
        'media_id': os.path.join(work_dir, 'media_id.txt'),
        'workloads': os.path.join(work_dir, 'workloads.json'),
    }
    return paths

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # Parse arguments.
    args = parse_args()

    # Get file paths.
    paths = get_file_paths(args.url, args.work_dir)

    # Download the file.
    subprocess.run(['wget', '-O', paths['original'], args.url])

    # Get md5 for the file.
    md5 = md5sum(args.url, args.size)

    # Get base filename.
    if args.name:
        name = args.name
    else:
        name = os.path.basename(paths['original'])

    # Determine transcodes that need to be done.
    workloads = determine_transcode(args.host, args.token, args.type, paths['original'],
                                    args.group_to)
    for workload in workloads:
        workload['configs'] = ','.join(workload['configs'])
    with open(paths['workloads'], 'w') as f:
        json.dump(workloads, f)

    # Create the media object.
    if args.media_id == -1:
        media_id = create_media(args.host, args.token, args.project, args.type, args.section,
                                name, md5, args.gid, args.uid, args.attributes)
    else:
        media_id = args.media_id

    with open(paths['media_id'], 'w') as f:
        f.write(str(media_id))

    # Make thumbnails.
    make_thumbnails(args.host, args.token, media_id, paths['original'], paths['thumbnail'],
                    paths['thumbnail_gif'])


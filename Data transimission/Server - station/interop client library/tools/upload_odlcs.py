# Module to load odlcs from file and upload via interoperability.

import logging
import os
import pprint
from auvsi_suas.proto import interop_api_pb2
from google.protobuf import json_format

logger = logging.getLogger(__name__)


def upload_odlc(client, odlc_file, image_file):
    """Upload a single odlc to the server

    Args:
        client: interop.Client connected to the server
        odlc_file: Path to file containing odlc details in the Object
            File Format.
        image_file: Path to odlc thumbnail. May be None.
    """
    odlc = interop_api_pb2.Odlc()
    with open(odlc_file) as f:
        json_format.Parse(f.read(), odlc)

    logger.info('Uploading odlc %s: %r' % (odlc_file, odlc))
    odlc = client.post_odlc(odlc).result()

    if image_file:
        logger.info('Uploading odlc thumbnail %s' % image_file)
        with open(image_file, 'rb') as img:
            client.post_odlc_image(odlc.id, img.read()).result()
    else:
        logger.warning('No thumbnail for odlc %s' % odlc_file)


def upload_odlcs(client, odlc_dir):
    """Upload all odlcs found in directory

    Args:
        client: interop.Client connected to the server
        odlc_dir: Path to directory containing odlc files in the Object
            File Format and odlc thumbnails.
    """
    odlcs = {}
    images = {}

    for entry in os.listdir(odlc_dir):
        name, ext = os.path.splitext(entry)

        if ext.lower() == '.json':
            if name in odlcs:
                raise ValueError(
                    'Found duplicate odlc files for %s: %s and %s' %
                    (name, odlcs[name], entry))
            odlcs[name] = os.path.join(odlc_dir, entry)
        elif ext.lower() in ['.png', '.jpg', '.jpeg']:
            if name in images:
                raise ValueError(
                    'Found duplicate odlc images for %s: %s and %s' %
                    (name, images[name], entry))
            images[name] = os.path.join(odlc_dir, entry)

    pairs = {}
    for k, v in odlcs.items():
        if k in images:
            pairs[v] = images[k]
        else:
            pairs[v] = None

    logger.info('Found odlc-image pairs:\n%s' % pprint.pformat(pairs))

    for odlc, image in pairs.items():
        upload_odlc(client, odlc, image)

import requests
import math
import os
import logging
import requests
import time

import tator

logger = logging.getLogger(__name__)

def _upload_file(api, project, path, media_id=None, filename=None, chunk_size=1024*1024*10, file_size=None):
    """ Uploads a file.

    :param api: `tator.TatorApi` object.
    :param project: Unique integer identifying a project.
    :param path: Path to file on disk.
    :param media_id: [Optional] Media ID if this is an upload for existing media.
    :param filename: [Optional] Filename (only used if media ID is given).
    :param chunk_size: [Optional] Upload chunk size in bytes.
    """
    MAX_RETRIES = 10 # Maximum retries on a given chunk.

    # Get number of chunks.
    if file_size is None:
        file_size = os.stat(path).st_size
    num_chunks = math.ceil(file_size / chunk_size)
    if num_chunks > 10000:
        chunk_size = math.ceil(file_size / 9000)
        logger.warning(f"Number of chunks {num_chunks} exceeds maximum of 10,000. Increasing "
                        "chunk size to {chunk_size}.")
        num_chunks = math.ceil(file_size / chunk_size)

    if path.startswith('https://') or path.startswith('http://') and filename:
        filename = filename.split('?')[0]
    # Get upload info.
    upload_kwargs = {'num_parts': num_chunks}
    if media_id is not None:
        upload_kwargs['media_id'] = media_id
    if filename is not None:
        upload_kwargs['filename'] = filename
    upload_info = api.get_upload_info(project, **upload_kwargs)

    # Functor to wrap around file versus URL
    def get_data(path):
        if path.startswith('https://') or path.startswith('http://'):
            return requests.get(path, stream=True).raw
        else:
            return open(path, 'rb')
    if num_chunks > 1:
        # Upload parts.
        parts = []
        last_progress = 0
        yield (last_progress, None)
        with get_data(path) as f:
            for chunk_count, url in enumerate(upload_info.urls):
                file_part = f.read(chunk_size)
                for attempt in range(MAX_RETRIES):
                    try:
                        response = requests.put(url, data=file_part)
                        etag = response.headers['ETag']
                        parts.append({'ETag': etag, 'PartNumber': chunk_count + 1})
                        break
                    except Exception as e:
                        logger.warning(f"Upload of {path} chunk {chunk_count} failed ({e})! Attempt "
                                       f"{attempt + 1}/{MAX_RETRIES}")
                        if attempt == MAX_RETRIES - 1:
                            raise Exception(f"Upload of {path} failed!")
                this_progress = round((chunk_count / num_chunks) *100,1)
                if this_progress != last_progress:
                    yield (this_progress, None)
                    last_progress = this_progress

        # Complete the upload.
        completed = False
        count = 0
        while completed is False and count < 5:
            try:
                count += 1
                response = api.complete_upload(project, upload_completion_spec={
                    'key': upload_info.key,
                    'upload_id': upload_info.upload_id,
                    'parts': parts,
                })
                if not isinstance(response, tator.models.MessageResponse):
                    raise Exception(f"Upload completion failed!")
                completed=True
            except Exception as e:
                print(e)
                time.sleep(2)
                completed = False
    else:
        # Upload in single request.
        with get_data(path) as f:
            data = f.read()
            for attempt in range(MAX_RETRIES):
                response = requests.put(upload_info.urls[0], data=data)
                if response.status_code == 200:
                    break
                else:
                    logger.warning(f"Upload of {path} failed ({response.text}) size={len(data)}! Attempt "
                                   f"{attempt + 1}/{MAX_RETRIES}")
                    if attempt == MAX_RETRIES - 1:
                        raise Exception(f"Upload of {path} failed!")

    # Return the parts and upload info.
    yield (100, upload_info)


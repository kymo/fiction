import os
import sys
import time
import datetime
import zipfile
import mimetypes
import shutil
from os import sep

import S3

import config

def zipit(file_path):
    zip_name = getZipFileName(zip_prefix)
    zip_file = file_path
    zip = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    zip.write(file_name)
    zip.close()
     
    # File Operations #
    os.remove(file_name)
    mv_to_path = os.path.join(copy_dir, zip_name)
    mv_to_dir = sep.join(mv_to_path.split(sep)[:-1])
    if not os.access(mv_to_dir, os.F_OK):
        os.makedirs(mv_to_dir)
    if os.access(mv_to_path, os.F_OK):
        os.remove(mv_to_path)
    shutil.copy(zip_file, mv_to_path)
    return zip_name


def read_data(file_object):
    while True:
        r = file_object.read(64 * 1024)

        if not r:
            break
        yield r

def S3Upload(upload_name, fileObj, bucket_name=None):
    print 'check upload args'
    if not bucket_name:
        raise ValueError('No Bucket Name')

    print 'conn'
    conn = S3.AWSAuthConnection(config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY)

    content_type = mimetypes.guess_type(upload_name)[0]
    if not content_type:
        content_type = 'text/plain'
    print 'conn put'
    st = conn.put(bucket_name, upload_name, S3.S3Object(fileObj),
        {'x-amz-acl': 'public-read', 'Content-Type': content_type})
    print 'end conn put'
    resp = st.http_response
    print 'resp', resp, resp.status
    if 200 != resp.status:
        print 'upload failed'
        print resp.msg
        return False
    print 'upload successed'
    return True

from . import *
from northgravity.Authenticator import Authenticator
import time

import requests
import logging
log = logging.getLogger('NG SDK')


class HTTPCaller:
    def __init__(self):
        self.url = ENDPOINT
        self.jobid = JOB_ID
        self.eid = EID
        self.token = Authenticator().get_token()

    def post(self, path, payload=None, data=None, headers=None):
        if headers is None:
            headers = {}
        # adding token to the headers
        headers.update(self.token)
        headers.update({"X-KH-JOB-ID": self.jobid})

        log.debug(f'Sending POST request to {path}, with payload: {payload}')
        r = requests.post(self.url + path, json=payload, data=data, headers=headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            log.info('Posting with message {} was successful with response: {}'.format(payload, r.text))
            return r

        else:
            log.error('Posting with message {} ended with error (error code: {}). Response: {}'.format(payload, r.status_code, r.text))
            return r

    def get(self, path, headers=None):
        # adding token to the headers
        if headers is None:
            headers = {}
        headers.update(self.token)
        headers.update({"X-KH-JOB-ID": self.jobid})

        full_path = self.url + path

        r = requests.get(full_path, headers=headers)

        log.debug(f'GET \n{r.url} \nHeaders: {r.request.headers}')

        if (r.status_code >= 200) and (r.status_code < 300):
            log.debug('Data received from {} with response: {}'.format(path, r.text))
            return r

        else:
            log.error('Data reception from {} ended with error (error code: {}). Response: {}'.format(path, r.status_code, r.text))
            return r

    def file_uploader(self, payload, file_path, headers=None):
        if headers is None:
            headers = {}
        # adding token to the headers
        headers.update(self.token)
        headers.update({'X-KH-JOB-ID': JOB_ID})

        # send meta data
        file_params_json = self.post('/file', payload, headers=headers).json()
        log.debug(file_params_json)
        url = file_params_json['location']
        file_id = file_params_json['fileId']

        file_content = open(file_path, 'rb').read()

        r = requests.put(url,
                         data=file_content,
                         headers={'Content-Type': 'application/octet-stream'}
                         )

        log.debug(f'PUT {r.url} \nHEADERS: {r.request.headers}')

        if (r.status_code >= 200) and (r.status_code < 300):

            # wait and ping every 10 seconds where the upload is finished - up to 10 times
            i = 0
            while i < 10:
                r_sync_ = self.get('/file/search?size=1&from=0&query=uuid%3D{}'.format(file_id), headers=headers)

                r_sync = r_sync_.json()

                i += 1
                log.debug(f'Search the uploaded file for the {i} time')

                # if nothing in items than wait 10 seconds
                if r_sync['items'] == []:
                    # if it is 10hth wait, something is wrong and exception is thrown
                    if i == 10:
                        raise Exception(f"File {file_id} upload is not successful after 100 seconds of waiting")
                    time.sleep(10)
                # otherwise items are not empty and file is successfully uploaded
                else:
                    log.debug(r_sync['items'])
                    log.info('File uploaded')
                    break

        return file_id

    def get_from_S3(self, S3path):
        r = requests.get(S3path)

        log.debug(f'GET form S3: {S3path}')

        if (r.status_code >= 200) and (r.status_code < 300):
            log.debug('File downloaded from {}'.format(S3path))
            return r

        else:
            log.error('File download from {} ended with error (error code: {}). Response: {}'.format(S3path, r.status_code, r.text))
            return r

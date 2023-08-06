'''An self-contained image.'''


import json as js
import numpy as np
import base64
import turbojpeg as tj
_tj = tj.TurboJPEG()


__all__ = ['PixelFormat', 'Image']



PixelFormat = {
    'rgb': (tj.TJPF_RGB, 3),
    'bgr': (tj.TJPF_BGR, 3),
    'rgba': (tj.TJPF_RGBA, 4),
    'gray': (tj.TJPF_GRAY, 1),
}


class Image(obj):
    '''A self-contained image, where the meta-data associated with the image are kept together with the image itself.

    Parameters
    ----------
    image : numpy.array
        a 2D image of shape (height, width, nchannels) or (height, width) with dtype uint8
    pixel_format : str
        one of the keys in the PixelFormat mapping
    meta : dict
        A JSON-like object. It holds additional keyword parameters associated with the image.
    '''
    
    def __init__(self, image, pixel_format='rgb', meta={}):
        self.image = image
        self.pixel_format = pixel_format
        self.meta = meta

    def check(self):
        '''Checks for data consistency, raising a ValueError if something has gone wrong.'''
        if len(self.image.shape) == 2:
            if self.pixel_format != 'gray':
                raise ValueError("Pixel format is not 'gray' but image has only one channel.")
            self.image = self.image.reshape(self.image.shape + (1,))
        elif len(self.image.shape) == 3:
            desired_nchannels = PixelFormat[self.pixel_format][1]
            if self.image.shape[2] != desired_nchannels:
                raise ValueError("Unexpected number of channels {}. It should be {} for pixel format '{}'.".format(self.image.shape[2], desired_nchannels, self.pixel_format))
        else:
            raise ValueError("Unexpected image shape {}. It must have 2 or 3 dimensions.".format(self.image.shape))

    # ---- serialisation -----

    def to_json(self, quality=90):
        '''Dumps the image to a JSON-like object.

        Parameters
        ----------
        quality : int
            percentage of image quality. Default is 90.

        Returns
        -------
        json_obj : dict
            the serialised json object
        '''

        # meta
        json_obj = {}
        json_obj['pixel_format'] = self.pixel_format
        json_obj['height'] = self.image.shape[0]
        json_obj['width'] = self.image.shape[1]
        json_obj['meta'] = meta

        # image
        img_bytes = _tj.encode(self.image, quality=quality, pixel_format=PixelFormat[self.pixel_format][0])
        encoded = base64.b64encode(img_bytes)
        json_obj['image'] = encoded.decode('ascii')

        return json_obj

    @staticmethod
    def from_json(json_obj):
        '''Loads the image from a JSON-like object produced by :func:`dumps`.

        Parameters
        ----------
        json_obj : dict
            the serialised json object

        Returns
        -------
        Image
            the loaded image with metadata
        '''

        # meta
        pixel_format = json_obj['pixel_format']
        meta = json_obj['meta']

        decoded = base64.b64decode(json_obj['image'])
        image = _tj.decode(decoded, pixel_format=pixel_format)

        return Image(image, pixel_format=pixel_format, meta=meta)

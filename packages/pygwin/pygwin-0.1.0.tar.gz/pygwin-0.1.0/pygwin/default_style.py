#!/usr/bin/env python3

'''@TODO@'''

import os
import logging
import pkg_resources

from . import StyleClass, Window


class DefaultStyle:  # pylint: disable=R0903
    '''@TODO@'''

    @classmethod
    def load(cls):
        '''@TODO@'''

        data_dir = pkg_resources.resource_filename('pygwin', 'data')

        #  load default style
        json = os.path.join(data_dir, 'default-style.json')
        if not os.path.isfile(json):
            logging.warning('default file %s not found!', json)
        else:
            StyleClass.load(json)

        #  load window cross image
        image = os.path.join(data_dir, 'window-cross.png')
        if os.path.isfile(image):
            StyleClass.get(Window).set_attr('image-window-cross', image)

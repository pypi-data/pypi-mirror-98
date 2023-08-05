"""Handlers for honeybee and dragonfly models."""
import os
import json

from honeybee.model import Model
from dragonfly.model import Model as ModelDF

from .helper import get_tempfile


def model_to_json(model_obj):
    """Translate a Honeybee model to a HBJSON file.

        Args:
            model_obj: Either a Honeybee model or the path to the HBJSON file.
                In case the model_obj is a path, it will be returned as is. For a
                Model object, it will be saved to a HBJSON file in a temp folder.

        Returns:
            str -- Path to HBJSON file.
    """
    if isinstance(model_obj, str):
        if not os.path.isfile(model_obj):
            raise ValueError('Invalid file path: %s' % model_obj)
        hb_file = model_obj
    elif isinstance(model_obj, Model):
        hb_file = get_tempfile('hbjson', model_obj.identifier)
        # write the dictionary into a file
        obj_dict = model_obj.to_dict()
        with open(hb_file, 'w') as fp:
            json.dump(obj_dict, fp)
    else:
        raise ValueError(
            'Model input should be a string or a Honeybee Model. '
            'Not {}.'.format(type(model_obj))
        )
    return hb_file


def model_dragonfly_to_json(model_obj):
    """Translate a Dragonfly model to a DFJSON file.

        Args:
            model_obj: Either a Dragonfly model or the path to the DFJSON file.
                In case the model_obj is a path, it will be returned as is.  For a
                Model object, it will be saved to a DFJSON file in a temp folder.

        Returns:
            str -- Path to DFJSON file.
    """
    if isinstance(model_obj, str):
        if not os.path.isfile(model_obj):
            raise ValueError('Invalid file path: %s' % model_obj)
        df_file = model_obj
    elif isinstance(model_obj, ModelDF):
        df_file = get_tempfile('dfjson', model_obj.identifier)
        # write the dictionary into a file
        obj_dict = model_obj.to_dict()
        with open(df_file, 'w') as fp:
            json.dump(obj_dict, fp)
    else:
        raise ValueError(
            'Model input should be a string or a Dragonfly Model. '
            'Not {}.'.format(type(model_obj))
        )
    return df_file

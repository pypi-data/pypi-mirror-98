import tensorflow as tf
from . import normalizer
from .label import Label
import os
import pickle
import shutil
from rs4 import pathtool, attrdict
import requests
from . import datasets

def get_latest_version (path):
    versions = [ int (v) for v in os.listdir (path) if v.isdigit () ]
    if not versions:
        raise ValueError ('cannot find any model')
    return sorted (versions) [-1]

def get_next_version (path):
    try:
        return get_latest_version (path) + 1
    except ValueError:
        return 1

def load_labels (asset_dir):
    labels_path = os.path.join (asset_dir, "labels")
    if not os.path.isfile (labels_path):
        return
    with open (labels_path, "rb") as f:
        labels = pickle.load (f)
        if str (labels [0].__class__).find ('dnn.label') != -1:
            convert_labels (asset_dir, labels)
            return load_labels (asset_dir)
    return [Label (*label) for label in labels]

def load_meta (asset_dir):
    _metafile = os.path.join (asset_dir, 'assets', 'meta')
    if os.path.isfile (_metafile):
        with open (_metafile, 'rb') as f:
            return pickle.loads (f.read ())

def save (model, model_dir, labels = [], assets_dir = None, verbose = True):
    if assets_dir and not labels:
        labels = load_labels (assets_dir)

    model.save (model_dir)
    if assets_dir:
        pathtool.mkdir (os.path.join (model_dir, 'assets'))
        verbose and print ("* Collecting assets")
        for asset in os.listdir (assets_dir):
            src = os.path.join (assets_dir, asset)
            if not os.path.isfile (src):
                continue
            verbose and print ('  - {} is copied'.format (asset))
            shutil.copyfile (src, os.path.join (model_dir, 'assets', asset))
convert = save

def deploy (model_dir, url, **data):
    with pathtool.flashfile ('model.zip') as zfile:
        pathtool.zipdir ('model.zip', model_dir)
        pathtool.uploadzip (url, 'model.zip', **data)
    resp = requests.get ('/'.join (url.split ("/")[:-2]))
    return resp.json ()

def load (model_dir):
    return Interpreter (model_dir)

def load_latest (path):
    return load (os.path.join (path, str (get_latest_version (path))))


class Interpreter:
    def __init__ (self, model_dir):
        self.model_dir = model_dir
        self.asset_dir = os.path.join (self.model_dir, 'assets')
        if not os.path.exists (self.asset_dir):
            self.asset_dir = self.model_dir
        self.model = tf.keras.models.load_model (model_dir, compile = False)
        self.normalizer = normalizer.Normalizer.load (self.asset_dir)
        self.labels = load_labels (self.asset_dir)
        self.meta = load_meta (self.asset_dir)

    def get_datasets (self):
        return datasets.load (os.path.join (self.model_dir, 'assets'))

    def normalize (self, x):
        if not self.normalizer:
            return x
        return self.normalizer.transform (x)

    def predict (self, *args, **kargs):
        return self.model.predict (*args, **kargs)

    def evaluate (self, *args, **kargs):
        return self.model.evaluate (*args, **kargs)


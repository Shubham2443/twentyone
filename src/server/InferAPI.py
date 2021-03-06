import yaml
from flask import Blueprint, request, jsonify
from base64 import b64decode, b64encode

import sys
sys.path.append("..")
import pandas as pd
from tasks.tasks import Task
from data.data import Data
from models.model import Model

import argparse
import yaml
import time
from pathlib import Path

import glob

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

sys.path.append("src/yolo")
from detect import detect

infer_api = Blueprint('infer_api', __name__)

config_path = "config/config.yaml"
with open(config_path, "r") as fp:
    config = yaml.load(fp, Loader=yaml.FullLoader)

@infer_api.route("/infer", methods = ['GET'])
def infer():
    # in the response you get task id and data, convert data to right format
    request_method = request.method

    res=None
    if request_method == "GET":
        file = request.files['file']
        # task_id = request.files['task_id']
        foo=file.filename
        print("File Name : ", foo)
        ext = foo.split(".")[-1]
        if ext == "xlsx":
            unparsedFile = file.read()
            dframe = pd.read_excel(file, index_col="date")
            data_config = jsonify(request.data)
            file_data = unparsedFile

            model = Model()
            location = config["model"]["save_location"]
            res = model.infer(location, "okP0KEPL", dframe)
        elif ext.lower() == "jpg":
            with torch.no_grad():
                res, text = detect(foo)

    return str(res)
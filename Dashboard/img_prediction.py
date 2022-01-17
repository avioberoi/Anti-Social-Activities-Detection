from __future__ import division, print_function
# coding=utf-8
import os
import torch
import easyocr

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename



# Model Saved
MODEL_PATH = './DLmodel.pth'

# Load your trained model
model = torch.load(MODEL_PATH)


def model_predict(img_path, model):
    
    reader = easyocr.Reader(['en'], gpu = False)
    result = reader.readtext(img_path,paragraph="False")

    text = ""
    for detection in result: 
        text = text + " " + detection[1]

    output = model.classify(img_path,text)
    hateful = "Yes" if output["label"] == 1 else "No"

    return hateful


def result():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        return preds
    return None


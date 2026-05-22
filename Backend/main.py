from fastapi import FastAPI
import cv2
import numpy as np

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello World!'}
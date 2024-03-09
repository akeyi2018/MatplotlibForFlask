# -*- coding: utf-8 -*-
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, send_file
import json


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def input():
    return 'HELLO'

@app.route('/show_graph',methods=["GET","POST"])
def hello():
    image = io.BytesIO()
    x = np.linspace(0, 10)
    y = np.sin(x)
    plt.plot(x, y)
    plt.savefig(image, format='png')
    image.seek(0)
    return send_file(image,
                     mimetype='image/png')
    # return send_file(image,
    #                  download_name="./image.png",
    #                  mimetype='image/png')

if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 18:47:22 2022

@author: rishi
"""

from flask import Flask, render_template, request, url_for, redirect
import pickle
import numpy as np
import pandas as pd
from werkzeug import security

model=pickle.load(open('cc.pkl','rb'))
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/predict_df', methods = ['POST', 'GET'])
def predict_df():
    if request.method == 'POST':
        f = request.files['File']
        if f.filename[-3:] != 'csv':
            return render_template('predict_df.html', pred1='Please provide csv file only!')
        f_path = "./files/" + f.filename
        f.save(f_path)
        df = pd.read_csv(f_path)
        prediction=model.predict(df)
        if prediction == 0:
            return render_template('predict_df.html', pred1='It seems to be an authentic transaction..')
        else:
            return render_template('predict_df.html', pred1='It seems to be a fraudulent transaction..')
        


@app.route('/predict_val',methods=['POST','GET'])
def predict_val():
    features=[float(x) for x in request.form.values()]
    final=[np.array(features)]
    print(features)
    print(final)
    prediction=model.predict(final)
    if prediction == 0:
        return render_template('predict_val.html', pred='It seems to be an authentic transaction')
    else:
        return render_template('predict_val.html', pred='It seems to be a fraudulent transaction')

if __name__ == "__main__":
    app.run(port=3000, debug=True)
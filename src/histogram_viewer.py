import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

extensions    = ['csv']
upload_dir    = 'uploaded_files'
histogram_dir = 'static/histograms'

matplotlib.use('Agg') #do not try to display the plot

def check_filename(filename):
    return filename.split(".")[-1] in extensions

def process_file(path):
    data      = pd.read_csv(path)
    img_name  = 'histogram_{0:%Y_%m_%d_%H_%M_%S}.png'.format(datetime.now())
    file_path = os.path.join(histogram_dir, img_name)
    data.hist(figsize=(20,20))
    plt.savefig(file_path)
    return file_path

@app.route("/", methods=['GET', 'POST'])
def upload():
    img_path = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        data_file = request.files['file']
        if data_file.filename == "":
            return redirect(request.url)
        if data_file and check_filename(data_file.filename):
            s_filename = secure_filename(data_file.filename)
            file_path  = os.path.join(upload_dir, s_filename)
            data_file.save(file_path)
            img_path = process_file(file_path)
    return render_template('index.html', hist_img_path = img_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

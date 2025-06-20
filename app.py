from flask import Flask, request, send_from_directory, send_file, redirect, url_for, render_template, jsonify
import os, subprocess, zipfile, io, math, threading, time
from PIL import Image

app = Flask(__name__)
DOWNLOAD_DIR = "./downloads"
progress = {"status": "idle", "percent": 0}

def run_scraper(url, min_w, min_h, max_w, max_h):
    progress["status"] = "running"
    progress["percent"] = 0
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    for f in os.listdir(DOWNLOAD_DIR):
        os.remove(os.path.join(DOWNLOAD_DIR, f))
    proc = subprocess.Popen(['gallery-dl', '-d', DOWNLOAD_DIR, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while proc.poll() is None:
        time.sleep(1)
        progress["percent"] = min(95, progress["percent"] + 5)
    filter_images(min_w, min_h, max_w, max_h)
    progress["status"] = "done"
    progress["percent"] = 100

def filter_images(min_width, min_height, max_width, max_height):
    for root, _, files in os.walk(DOWNLOAD_DIR):
        for filename in files:
            path = os.path.join(root, filename)
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    if not (min_width <= w <= max_width and min_height <= h <= max_height):
                        os.remove(path)
            except:
                os.remove(path)
    return
#
    for filename in os.listdir(DOWNLOAD_DIR):
        path = os.path.join(DOWNLOAD_DIR, filename)
        try:
            with Image.open(path) as img:
                w, h = img.size
                if not (min_width <= w <= max_width and min_height <= h <= max_height):
                    os.remove(path)
        except:
            os.remove(path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    min_width = int(request.form['min_width'])
    min_height = int(request.form['min_height'])
    max_width = int(request.form['max_width'])
    max_height = int(request.form['max_height'])
    per_page = int(request.form['per_page'])
    threading.Thread(target=run_scraper, args=(url, min_width, min_height, max_width, max_height)).start()
    return redirect(url_for('loading', per_page=per_page))

@app.route('/loading')
def loading():
    per_page = request.args.get('per_page', 20)
    return render_template('loading.html', per_page=per_page)

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/gallery')
def gallery():
    files = []
    for root, _, filenames in os.walk(DOWNLOAD_DIR):
        for name in filenames:
            files.append(os.path.relpath(os.path.join(root, name), DOWNLOAD_DIR))
    if not files:
        return "No images found.<br><a href='/'>← Go back</a>"
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    total_pages = max(1, math.ceil(len(files) / per_page))
    start = (page - 1) * per_page
    end = start + per_page
    files_to_show = files[start:end]
    return render_template('gallery.html', files=files_to_show, page=page, per_page=per_page, total_pages=total_pages)

@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory(DOWNLOAD_DIR, filename)

@app.route('/download')
def download_zip():
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for filename in os.listdir(DOWNLOAD_DIR):
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            zf.write(filepath, arcname=filename)
    mem_zip.seek(0)
    return send_file(mem_zip, mimetype='application/zip', as_attachment=True, download_name='images.zip')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

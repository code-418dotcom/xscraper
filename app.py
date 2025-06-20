from flask import Flask, request, send_from_directory, send_file, redirect, url_for, render_template, jsonify
import os
import shutil
import subprocess
import zipfile
import io
import math
import threading
import itertools
from PIL import Image

app = Flask(__name__)
DOWNLOAD_DIR = "./downloads"
progress = {"status": "idle", "percent": 0}

HTML_COUNTER = itertools.count()

def scrape_with_soup(url, visited=None, depth=0, max_depth=2, root_url=None):
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlparse

    if visited is None:
        visited = set()
    if root_url is None:
        root_url = url
    if depth > max_depth or url in visited:
        return
    visited.add(url)

    html_dir = os.path.join(DOWNLOAD_DIR, "html")
    os.makedirs(html_dir, exist_ok=True)
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        img_tags = soup.find_all("img")
        for img in img_tags:
            src = img.get("src")
            if not src:
                continue
            img_url = urljoin(url, src)
            try:
                img_data = requests.get(img_url, timeout=10).content
                ext = os.path.splitext(img_url)[1] or ".jpg"
                fname = f"img_{next(HTML_COUNTER)}{ext}"
                with open(os.path.join(html_dir, fname), "wb") as f:
                    f.write(img_data)
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

        if depth < max_depth:
            root_domain = urlparse(root_url).netloc
            for link in soup.find_all("a", href=True):
                href = urljoin(url, link["href"])
                if urlparse(href).netloc == root_domain and href not in visited:
                    scrape_with_soup(href, visited, depth + 1, max_depth, root_url)
    except Exception as e:
        print(f"Soup scraping failed for {url}: {e}")


def run_scraper(url, min_w, min_h, max_w, max_h):
    progress["status"] = "running"
    progress["percent"] = 0

    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    subprocess.run(
        ["gallery-dl", "--config", "gallery-dl.conf", "-d", DOWNLOAD_DIR, url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    has_files = any(
        os.path.isfile(os.path.join(root, f))
        for root, _, files in os.walk(DOWNLOAD_DIR)
        for f in files
    )
    if not has_files:
        scrape_with_soup(url)

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

@app.route('/')
def home():
 wpqyrg-codex/find-and-fix-bugs-in-codebase

        for root, _, files in os.walk(DOWNLOAD_DIR):
            for filename in files:
                filepath = os.path.join(root, filename)
                arcname = os.path.relpath(filepath, DOWNLOAD_DIR)
                zf.write(filepath, arcname=arcname)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
 main

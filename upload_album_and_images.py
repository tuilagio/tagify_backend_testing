import requests
import json
import os
from os import listdir
from os.path import isfile, join
import zipfile
import shutil

base_url = "http://127.0.0.1:5000/api"
s = requests.Session()
data = {"username": "user", "password": "user"}

### Login
r = s.post(f"{base_url}/login", json=data)

## Print cookies
# print(s.cookies)
## Testing:
# r = s.get("http://127.0.0.1:5000/api/user/me")
# print(r.json())

### Extract data
path_temp = "temp"
if not os.path.exists(path_temp):
    os.mkdir(path_temp)
id_path = join(path_temp, "images_data")
if not os.path.exists(id_path):
    os.mkdir(id_path)

onlyfiles = [f for f in listdir("imgs_data") if isfile(join("imgs_data", f))]
for path in onlyfiles:
    if path.split(".")[-1] == "zip":
        with zipfile.ZipFile(join("imgs_data", path),"r") as zip_ref:
            print(f"Extracting {join('imgs_data', path)} to {join(path_temp, 'images_data')}")
            zip_ref.extractall(id_path)

##  Create some albums
list_album = os.listdir(id_path)
for album_folder in list_album:
    # Read meta:
    with open(join(id_path, album_folder, "meta.txt")) as meta_file:
        meta_json = json.load(meta_file)
        # Create album
        r = s.post(f"{base_url}/user/albums", json=meta_json)
        if r.status_code == 200:
            album_id = (r.json()["id"])
            print(f"Created album with  id = {album_id}")
            # Upload images:
            images_path = join(id_path, album_folder, "images")
            onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]
            for img_path in onlyfiles:
                files = {'fieldName': open(join(images_path, img_path), 'rb')}
                r = s.post(f"{base_url}/user/albums/{album_id}/photos", files=files)

    ### TODO: remove extracted data
    # shutil.rmtree(join(id_path, album_folder))
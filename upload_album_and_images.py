import requests
import json
import os
from os import listdir
from os.path import isfile, join
import zipfile

headers = {'Content-type': 'application/json'}
base_url = "http://127.0.0.1:5000/api"
s = requests.Session()
data = {"username": "user", "password": "user"}
r = s.post(f"{base_url}/login", json=data)

# print(s.cookies)
# print(r)
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





# apparent_encoding 	
# Returns the apparent encoding
# close() 	
# Closes the connection to the server
# content 	
# Returns the content of the response, in bytes
# cookies 	
# Returns a CookieJar object with the cookies sent back from the server
# elapsed 	
# Returns a timedelta object with the time elapsed from sending the request to the arrival of the response
# encoding 	
# Returns the encoding used to decode r.text
# headers 	
# Returns a dictionary of response headers
# history 	
# Returns a list of response objects holding the history of request (url)
# is_permanent_redirect 	
# Returns True if the response is the permanent redirected url, otherwise False
# is_redirect 	
# Returns True if the response was redirected, otherwise False
# iter_content() 	
# Iterates over the response
# iter_lines() 	
# Iterates over the lines of the response
# json() 	
# Returns a JSON object of the result (if the result was written in JSON format, if not it raises an error)
# links 	
# Returns the header links
# next 	
# Returns a PreparedRequest object for the next request in a redirection
# ok 	
# Returns True if status_code is less than 200, otherwise False
# raise_for_status() 	
# If an error occur, this method returns a HTTPError object
# reason 	
# Returns a text corresponding to the status code
# request 	
# Returns the request object that requested this response
# status_code 	
# Returns a number that indicates the status (200 is OK, 404 is Not Found)
# text 	
# Returns the content of the response, in unicode
# url 	
# Returns the URL of the response
import csv
from zipfile import ZipFile
from io import TextIOWrapper, BytesIO
import requests

resp = requests.get('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', stream=True)
urls = []  # top 1 million URL's will be stored in this list
with ZipFile(BytesIO(resp.content)) as zf:
    csv_filename = zf.namelist()[0]
    with zf.open(csv_filename) as csv_file:
        for _, website in csv.reader(TextIOWrapper(csv_file)):
            urls.append('http://' + website)

import sys
import tempfile
import urllib.request
import shutil
import camelot
import json
from fuzzywuzzy import fuzz



base_url = "https://www.mediapeta.com/peta/PDF/"

def refresh_list(list_type):
    url = f"{base_url}{list_type}.pdf"
    data = list()
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with tempfile.NamedTemporaryFile(suffix='.pdf') as pdf_file, urllib.request.urlopen(request) as response:
        shutil.copyfileobj(response, pdf_file)
        tables = camelot.read_pdf(pdf_file.name, pages='1-end', flavor='stream')
        for table in tables:
            if table.df.columns.stop <= 1:
                continue
            for row in table.df.itertuples():
                company = "".join(row[1:4]).lower()
                data.append(company)
    with open(f"{list_type}.json", 'w') as outfile:
        json.dump(data, outfile)
    
if __name__ == "__main__":
    refresh_list("companiesdonttest")
    refresh_list("companiesdotest")
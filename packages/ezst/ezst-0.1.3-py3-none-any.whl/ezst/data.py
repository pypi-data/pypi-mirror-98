import os
import zipfile
import requests

def load(dataset_name):

  if( dataset_name == 'cats_dogs'):
    save_path = './cats_dogs.zip'
    url = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

    local_zip = 'cats_dogs.zip'

    zip_ref = zipfile.ZipFile(local_zip, 'r')

    zip_ref.extractall('./')
    zip_ref.close()

    os.remove("cats_dogs.zip")
    os.rename('cats_and_dogs_filtered', 'cats_dogs')

  else:
    print('지원하지 않는 데이터셋 입니다.')
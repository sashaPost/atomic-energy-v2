from django.core.files.storage import Storage
import requests 



class CDNStorage(Storage):
    def __init__(self, cdn_url):
        self.cdn_url = cdn_url

    def save(self, name, content):
        url = f"{self.cdn_url}/{name}"
        try:
            response = requests.put(url, data=content.read())
            if response.status_code != 200:
                raise IOError(f"Failed to upload file to CDN: {response.status_code}")
            return name
        except Exception as e:
            print(f"Exception during CDN upload: {e}")
            raise IOError("Failed to upload file to CDN")
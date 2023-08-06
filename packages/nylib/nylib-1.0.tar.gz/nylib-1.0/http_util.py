import requests


def download_mini(url, file):
    r = requests.get(url)  # create HTTP response object
    with open(file, 'wb') as f:
        f.write(r.content)


def download(url, file):
    r = requests.get(url, stream=True)
    with open(file, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


if __name__ == '__main__':
    image_url = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
    # download_mini(image_url, "python_logo.png")
    download(image_url, "python_logo.png")

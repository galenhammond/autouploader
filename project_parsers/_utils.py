def download(url, path):
    """
    Download a file from a URL to a given path
    """
    import requests
    import os

    # Create the path if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Get the file name from the URL
    file_name = url.split("/")[-1]

    # Create the full path to the file
    full_path = os.path.join(path, file_name)

    # Download the file
    r = requests.get(url, stream=True)
    with open(full_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return full_path

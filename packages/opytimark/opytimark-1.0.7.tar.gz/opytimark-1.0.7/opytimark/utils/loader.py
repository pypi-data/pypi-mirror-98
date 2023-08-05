"""Auxiliary files loader.
"""

import os
import tarfile
import urllib.request

import numpy as np

import opytimark.utils.constants as c


def download_file(url, output_path):
    """Downloads a file given its URL and the output path to be saved.

    Args:
        url (str): URL to download the file.
        output_path (str): Path to save the downloaded file.

    """

    # Checks if file exists
    file_exists = os.path.exists(output_path)

    # If file does not exist
    if not file_exists:
        # Checks if data folder exists
        folder_exists = os.path.exists(c.DATA_FOLDER)

        # If data folder does not exist
        if not folder_exists:
            # Creates the folder
            os.mkdir(c.DATA_FOLDER)

        # Downloads the file
        urllib.request.urlretrieve(url, output_path)


def untar_file(file_path):
    """De-compress a file with .tar.gz.

    Args:
        file_path (str): Path of the file to be de-compressed.

    Returns:
        The folder that has been de-compressed.

    """

    # Opens a .tar.gz file with `file_path`
    with tarfile.open(file_path, "r:gz") as tar:
        # Defines the path to the folder
        folder_path = file_path.split('.tar.gz')[0]

        # Extracts all files
        tar.extractall(path=folder_path)

    return folder_path


def load_cec_auxiliary(name, year):
    """Loads auxiliary data for CEC-based benchmarking functions.

    Args:
        name (str): Name of function to be loaded.
        year (str): Year of function to be loaded.

    Returns:
        An array holding the auxiliary data.

    """

    # Defines some common-use variables
    base_url = 'http://recogna.tech/files/opytimark/'
    tar_name = f'{year}.tar.gz'
    tar_path = f'data/{tar_name}'

    # Downloads the file
    download_file(base_url + tar_name, tar_path)

    # De-compresses the file
    folder_path = untar_file(tar_path)

    # Loads the auxiliary data
    data = np.loadtxt(f'{folder_path}/{name}.txt')

    return data

"""Module for extracting space weather data fetched from SWPC
"""

import logging
import re

import numpy as np
import pandas as pd

from vinvelivaanilai.storage.common import set_datetime_index

LOGGER = logging.getLogger(__name__)
CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
CH.setFormatter(FORMATTER)
LOGGER.addHandler(CH)


# pylint: disable=too-many-locals
def extract_data_regex(name, path_to_file):
    """Extracts data from path_to_file based on name

    Args:
        name (str): One of dgd, dpd, dsd
        path_to_file (str): Path to file containing data

    Raises:
        ValueError: If name is not in ("dgd", "dpd", "dsd")
        ValueError: If no match is found in data

    Returns:
        pd.DataFrame: DataFrame containing all the data
    """
    date = r"^(\d{4} *\d{2} *\d{2}) *"

    if name.strip().lower() == "dpd":
        column_dict = {
            "Date": "",
            "Proton 1 MeV": "-1.0e+00",
            "Proton 10 MeV": "-1.0e+00",
            "Proton 100 MeV": "-1.0e+00",
            "Electron 800 KeV": "-1.0e+00",
            "Electron 2 MeV": "-1.0e+00",
            "Neutron": "-999.99",
        }

        peindices = r"(-1\.0e\+00|\d*\.\d*e\+\d*) *"
        nindices = r"(-999\.99|-1|\d*\.\d*)$"
        regex = date + peindices * 5 + nindices

    elif name.strip().lower() == "dgd":
        column_dict = {
            "Date": "",
            "Fredericksburg A": "-1",
            "Fredericksburg K 0-3": "-1",
            "Fredericksburg K 3-6": "-1",
            "Fredericksburg K 6-9": "-1",
            "Fredericksburg K 9-12": "-1",
            "Fredericksburg K 12-15": "-1",
            "Fredericksburg K 15-18": "-1",
            "Fredericksburg K 18-21": "-1",
            "Fredericksburg K 21-24": "-1",
            "College A": "-1",
            "College K 0-3": "-1",
            "College K 3-6": "-1",
            "College K 6-9": "-1",
            "College K 9-12": "-1",
            "College K 12-15": "-1",
            "College K 15-18": "-1",
            "College K 18-21": "-1",
            "College K 21-24": "-1",
            "Planetary A": "-1",
            "Planetary K 0-3": "-1",
            "Planetary K 3-6": "-1",
            "Planetary K 6-9": "-1",
            "Planetary K 9-12": "-1",
            "Planetary K 12-15": "-1",
            "Planetary K 15-18": "-1",
            "Planetary K 18-21": "-1",
            "Planetary K 21-24": "-1",
        }
        aindices = r"(-1|\d{1,3}) *"
        kindices = r"(-1|\d{1}) *"
        regex = date + (aindices + kindices * 8) * 3 + r"$"

    elif name.strip().lower() == "dsd":
        column_dict = {
            "Date": "",
            "Radio Flux": "-1",
            "SESC sunspot number": "*",
            "Sunspot Area": "-1",
            "New Regions": "-1",
            "Solar Mean Field": "-999",
            "X-ray Background Flux": "*",
            "X-Ray C": "-1",
            "X-Ray M": "-1",
            "X-Ray X": "-1",
            "X-Ray S": "-1",
            "Optical 1": "-1",
            "Optical 2": "-1",
            "Optical 3": "-1",
        }
        # Radio Flux, Sunspot Area, New regions, Flares
        type1 = r"(-1|\d+) *"
        # SESC sunspot number,
        sunspot = r"(\*|\d+) *"
        # X-ray bgnd flux
        xrbflux = r"(\*|[AB]\d\.\d) *"
        # Solar mean field
        smfield = r"(-999|\d+) *"
        regex = (
            date + type1 + sunspot + type1 * 2 + smfield + xrbflux + type1 * 7
        )

    else:
        raise ValueError("The data {} is not supported yet".format(name))

    data = []

    with open(path_to_file) as file:
        LOGGER.info("Extracting data from %s", path_to_file)
        matches = re.finditer(regex, file.read(), re.MULTILINE)
        for match in matches:
            data.append(match.groups())

    if data == []:
        raise ValueError(
            "No data found in the file."
            "Are you sure the file name and type are correct?"
        )

    dataframe = pd.DataFrame(data, columns=column_dict.keys())
    dataframe = set_datetime_index(dataframe, "Date")

    null_value = ""
    for column in dataframe.columns:
        null_value = column_dict[column]
        dataframe[column] = pd.to_numeric(
            dataframe[column].apply(
                lambda x: np.nan if x == null_value else x
            ),
            errors="ignore",
        )

    return dataframe


def extract_data_from_multiple(name, path_to_files):
    """Extract data from multiple files

    Args:
        name (str): Name of the index in the file
        path_to_files (list): List containing paths to the files

    Returns:
        pd.DataFrame: Dataframe containing all the extracted data
    """
    if not name.strip().upper() in ("DGD", "DPD", "DSD"):
        raise ValueError("{} not in 'DGD', 'DSD', 'DPD'".format(name.upper()))

    if not isinstance(path_to_files, list):
        raise ValueError(
            "Expected {} got {} for path_to_files".format(
                list, type(path_to_files)
            )
        )

    dfs = []

    for file in path_to_files:
        dfs.append(extract_data_regex(name, file))

    return pd.concat(dfs)

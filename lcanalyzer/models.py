"""Module containing models representing lightcurves.

The Model layer is responsible for the 'business logic' part of the software.

The lightcurves are saved in a table (2D array) where each row corresponds to a single observation. 
Depending on the dataset (LSST or Kepler), a table can contain observations of a single or several 
objects, in a single or different bands.

Functions: 
  load_dataset - Load a table from CSV file
  mean_mag - Calculate the mean magnitude of a lightcurve
  max_mag - Calculate the max magnitude of a lightcurve
  min_mag - Calculate the min magnitude of a lightcurve
"""

import pandas as pd
#import numpy as np
#from astropy.timeseries import LombScargle

def normalize_lc(df,mag_col):
    """LC normalization.
    
    :param df: the DataFrame in question
    :param mag_col: the name of the DataFrame column in question
    :returns: array with normalized light curve .
    """
    # Normalize a single light curve
    if any(df[mag_col].abs() > 90):
        raise ValueError(mag_col+' contains values with abs() larger than 90!')
    brightest = min_mag(df,mag_col)
    faintest = max_mag((df-brightest),mag_col)
    lc = (df[mag_col]-brightest)/faintest
    lc = lc.fillna(0)
    return lc

def calc_stats(lc, bands, mag_col):
    """Calculate basic statistics for a DataFrame.
    
    :param lc: the DataFrame in question
    :param bands: list of bands to query
    :param mag_col: the name of the DataFrame column in question
    :returns: DataFrame with statistics: min, mean, max per band.
    """
    # Calculate max, mean and min values for all bands of a light curve
    stats = {}
    for b in bands:
        stat = {}
        stat["max"] = max_mag(lc[b], mag_col)
        stat["mean"] = mean_mag(lc[b], mag_col)
        stat["min"] = min_mag(lc[b], mag_col)
        stats[b] = stat
    return pd.DataFrame.from_records(stats)

def load_dataset(filename):
    """Load a table from CSV file.
    
    :param filename: The name of the .csv file to load
    :returns: pd.DataFrame with the data from the file.
    """
    return pd.read_csv(filename)


def mean_mag(data,mag_col):
    """Calculate the mean magnitude of a lightcurve

    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: specify column name in the columnmag_col in data.
    """
    return data[mag_col].mean()


def max_mag(data,mag_col):
    """Calculate the max magnitude of a lightcurve

    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: specify column name in data
    :returns: max value of of the column.
    """
    return data[mag_col].max()


def min_mag(data,mag_col):
    """Calculate the min magnitude of a lightcurve

    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the min value.
    :returns: The min value of the column.
    """
    return data[mag_col].min()

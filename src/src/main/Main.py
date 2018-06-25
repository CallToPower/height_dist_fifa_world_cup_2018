#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Distributions of height for the different positions in the 2018 FIFA World Cup
# Copyright 2018 Denis Meyer
# Data: Copyright 2018 FIFA
#

import logging
import requests
from tabula import read_pdf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Logging configuration
logging_loglevel = logging.DEBUG
logging_datefmt = '%d-%m-%Y %H:%M:%S'
logging_format = '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s'

# More options
# Newer versions available at 'https://img.fifa.com/image/upload/hzfqyndmnqazczvc5xdb.pdf'
inurl = 'https://dl.dropboxusercontent.com/s/ahf1o9z8ahetz8y/fifa_player_list.pdf?dl=0'
infile = 'fifa_player_list.pdf'
outfile = 'height_dist_fifa_world_cup_2018.png'
param_pos = 'POS'
param_height = 'Height'

def initialize_logger():
    logging.basicConfig(level=logging_loglevel,
                        format=logging_format,
                        datefmt=logging_datefmt)

def to_position(argument):
    switcher = {
        'GK': 'Goalkeeper',
        'DF': 'Defender',
        'MF': 'Midfielder',
        'FW': 'Forward'
    }
    return switcher.get(argument, 'Undefined')

def download(url, in_fname):
    r = requests.get(url, stream=True)
    with open(in_fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)

def read_data(in_fname):
    logging.debug('Reading data from "{}"'.format(in_fname))
    return read_pdf(in_fname, pages='all')

def clean_up(df):
    logging.debug('Cleaning up')
    positions = [name for name, group in df.groupby(param_pos)]
    try:
        del positions[positions.index(param_pos)]
    except ValueError:
        pass
    df_clean = df[df[param_pos].isin(positions)]
    df_clean = df_clean[df_clean[param_height].apply(lambda x: not pd.isnull(x) and (
        (type(x) == str and x.isnumeric()) or (type(x) == float == int or type(x) == float)))]
    df_clean[param_height] = df_clean[param_height].apply(pd.to_numeric)
    df_clean[param_pos] = df_clean[param_pos].apply(to_position)
    return df_clean

def plot(df, out_fname):
    logging.debug('Plotting')
    snsplot = sns.boxplot(y=param_height, x=param_pos,
                          data=df,
                          width=0.5,
                          palette='colorblind')
    snsplot = sns.stripplot(y=param_height, x=param_pos,
                            data=df,
                            jitter=True,
                            marker='o',
                            alpha=0.5,
                            color='black')
    snsplot.axes.set_title('Distributions of height for the different positions in the 2018 FIFA World Cup', fontsize=16)
    snsplot.set_xlabel('Position', fontsize=14)
    snsplot.set_ylabel('Height (in cm)', fontsize=14)
    snsplot.tick_params(labelsize=10)
    fig = snsplot.get_figure()
    fig.set_size_inches(12, 8)
    fig.savefig(out_fname)
    # plt.show()

if __name__ == '__main__':
    initialize_logger()

    download(inurl, infile)
    df = read_data(infile)
    df_clean = clean_up(df)
    plot(df_clean, outfile)

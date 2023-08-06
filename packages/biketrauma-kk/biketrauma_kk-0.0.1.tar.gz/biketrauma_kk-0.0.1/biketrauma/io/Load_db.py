import pandas as pd
from download import download
#from biketrauma.io import url_db, path_target
import os

url_db = "https://www.data.gouv.fr/fr/datasets/r/0d4eb9d0-2d80-44a0-9ff5-92ed53f59cdf"
path_target = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data", "bicycle_db.csv")

class Load_db:
  def __init__(self, url=url_db, target_name=path_target):
    download(url, target_name, replace=False)
  
  @staticmethod
  def save_as_df():
    df_bikes = pd.read_csv(path_target, na_values="", low_memory=False, converters={'data': str, 'heure': str})
    return df_bikes
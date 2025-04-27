import pandas as pd
import kagglehub
from pathlib import Path


class Data():
    def __init__(self, file_path):
        # Download latest version
        self.file_path = kagglehub.dataset_download(file_path)

    def get_df(self):
        return pd.read_csv(Path(self.file_path, "TWO_CENTURIES_OF_UM_RACES.csv"))


if __name__ == '__main__':
    my_data = Data("aiaiaidavid/the-big-dataset-of-ultra-marathon-running")

"""Questions database from CSV file."""

import os

import pandas as pd


# Path for the CSV file
PATH = os.path.abspath('db')
PATH_CSV = os.path.join(PATH, "questions.csv")


class DataQuestions:
    """Class to read the questionnary database."""
    
    def __init__(self):
        """Initiate the data from CSV and fill the NaN value with empty string.
        
        Attribute
        ---------
        df : DataFrame
            A DataFrame from a CSV file.
        """
        self.df = pd.read_csv(PATH_CSV)
        self.df = self.df.fillna('')
    
    @property
    def data(self):
        """Return the dataframe."""
        return self.df

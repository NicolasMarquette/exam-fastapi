"""CRUD to deal with the questionnary database."""

import os
import random

import pandas as pd

from db.db_questions import DataQuestions, PATH_CSV


# Path for the CSV file.
DATA = PATH_CSV

# Importation of the questions data.
df = DataQuestions().data


def get_uses():
    """Get all the unique test type in the database.

    Return
    ------
    uses : list
        A list with all the unique test type in the database.
    """
    uses = [u for u in df.use.unique()]
    return uses


def get_subject(use):
    """Get all the unique subjects for a specific test type.
    
    Return
    ------
    subjects : list
        A list with all the unique subject for a specific test type  in the database.
    """
    subjects = [s for s in df.subject[df.use == use].unique()]
    return subjects


def return_questions(use, subject, nombre):
    """Returns the questions according to the chosen test type and subjects.
    
    Parameters
    ----------
    use : str
        The test type  in the API request. 
    subjects : list
        The list of subjects in the API request.
    
    Return
    ------
    quest : dict
        A dictionnary with the questions and the answers to choose.
    """
    quest = dict()
    questions = [q for q in df.question[(df.use == use) & (df.subject.isin(subject))]]
    # Shuffle the questions to have a random return for each request.
    random.shuffle(questions)
    for i, v in enumerate(questions[:nombre]):
        quest.update({
            f"Question {i+1}": {
                "question": v,
                "A": df.loc[df.index[df.question == v], "responseA"].item(),
                "B": df.loc[df.index[df.question == v], "responseB"].item(),
                "C": df.loc[df.index[df.question == v], "responseC"].item(),
                # The question D appear only if the value is not empty in the database.
                **({
                    "D": df.loc[df.index[df.question == v], "responseD"].item()
                    } 
                if df.loc[df.index[df.question == v], "responseD"].item() != '' else {})
            }
        })
    return quest


def add_question(question):
    """Add the new question in the csv.
    
    Paramater
    ---------
    question : dict
        A dictionnary with the elements to add
    """
    dict_add = {k: [v] for k, v in question.items()}
    df_add = pd.DataFrame(dict_add)
    # Add the new question in the CSV file.
    df_add.to_csv(PATH_CSV, mode="a", index=False, header=False)


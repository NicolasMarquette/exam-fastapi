"""The user route"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List

from crud import crud_question as cq


ques = APIRouter()

# All the tests type in the database.
USES = cq.get_uses()


def verify_use(use: str = Query(None, description=f"Type of use : {', '.join(USES)}")):
    """Check if the test type is in the database.
    \f
    Parameter
    ---------
    use : str
        The type of test specified in the request

    Raise
    -----
    Error 404 : HTTPException
        Raise the error when the type of test is not in the base.

    Return
    use : str
        The type of test specified in the request
    ------
    """
    if use not in USES:
        raise HTTPException(
        status_code=404,
        detail=f"The type of test chosen is not in the database ({', '.join(USES)})"
        )
    return use


@ques.get("/uses", tags=["questions"], 
        name="Return a list of the test type in the database", 
        responses={
            401: {"description": "'Not authenticated"},
            404: {"description": "'Type of test not found in the base"}
        }
)
async def get_uses():
    """Get a list of all the test type in the database."""
    return USES


@ques.get("/subjects", 
        tags=["questions"], 
        name="Returns a list of subjects according to the specified test type",
        responses={
            401: {"description": "'Not authenticated"},
            404: {"description": "'Type of test not found in the base"}
        }
)
async def get_subjects(use: str = Depends(verify_use)):
    """Get a list of all the subjects according to the type of test indicated.
    \f
    Parameter
    ---------
    use : str
        The type of test specified in the request
    
    Return
    ------
    list : A list with all unique subjects for the type of test indicated.
    """
    return cq.get_subject(use)


@ques.get("/questions", 
        tags=["questions"], 
        name="Generate a questionnary",
        responses={
            401: {"description": "'Not authenticated"},
            404: {"description": "- Type of test not found in the database\n"
                                        + "- one or several subject not match the type of test selected\n"
                                        + "- number of questions indicated is not enought \
                                            or if the number of questions is not in [5, 10, 20]"}
        }
)
async def get_questions(
    nb_questions: int = Query(None, description="Number of questions for the questionnary"),
    use: str = Depends(verify_use), 
    subject: List[str] = Query(None, description="List of subjects")
):
    """Get a questionnary with the specified number of questions.
    \f
    Parameters
    ----------
    number_questions : int (path)
        Indicate the number of questions. Should be 5, 10 or 20.
    use : str (query)
        The type of test specified in the request 
    subject : List[str] (query)
        A list of subject according to the test type.
    
    Raises
    ------
    HTTPException : 404
        Raise an error when the type of test selected is not in the database.
    HTTPException : 404
        Raise an error if one or several subject not match the test type selected.
    HTTPException : 404
        Raise an error when the number of questions indicated is not enought 
        or if the number of questions is not in [5, 10, 20].
    
    Return
    ------
    questions : dict
        Return a dictionnary with the questions. 

    Example
    -------
    {
        "Question 1": {
            "question": "MongoDB et CouchDB sont des bases de données",
            "A": "relationnelles",
            "B": "orientées objet",
            "C": "orientées colonne",
            "D": "orientées graphe"
        }
    }
    """
    if (
        subject is not None 
        and all(item in cq.get_subject(use) for item in subject)
    ):
        questions = cq.return_questions(use, subject, nb_questions)
        if len(questions) in [5, 10, 20]:
            return questions
        raise HTTPException(
            status_code=404,
            detail="Not enought questions to generate a questionnary or wrong number of questions (5, 10 or 20)."
        )
    raise HTTPException(
        status_code=404,
        detail="One or several subjects not in the type selected."
    )

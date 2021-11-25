"""The admin API route"""

from fastapi import APIRouter

from models import question
from crud import crud_question as cq


admin = APIRouter()

@admin.post("/admin", name="Add a question in the base", 
    tags=["admin"], 
    status_code=201, response_model=question.QuestionIn,
    responses={401: {"description": "Unauthorized"}}
)
async def add_question(question: question.Question):
    """Create a question in the base with all the information.

    - **question**: str : the new question
    - **subject**: str : the subject of the question
    - **use**: str : the type of test for the question
    - **correct**: str : the correct answer
    - **responseA**: str : the response A in the multichoice
    - **responseB**: str : the response B in the multichoice
    - **responseC**: str : the response C in the multichoice
    - **responseD**: Optional[str] = None : the response D in the multichoice
    - **remark**: Optional[str] = None : the remark
    \f
    Parameter
    ---------
    User input

    Return
    ------
    dict : A dictionnary with the information entered and a message.

    """
    question_dict = question.dict()
    cq.add_question(question_dict)
    return {"status": "The new question was created",
            "created_item": question}

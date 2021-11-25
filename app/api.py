"""Run the API"""

from fastapi import FastAPI
from fastapi.param_functions import Depends

from router import admin, user
from authorization import security


description = """
## API to generate a questionnay

### questions (for enregistered users)

You can :

- Get all types of test in the database.
- Get all the subjects for the specified test type.
- Generate a questionnary with the specified number of questions, type of test and a list of subjects.

### admin

The personn with **admistrator rights** will be able to add new questions in the database.
"""

app = FastAPI(
    title="QUESTIONNARY API",
    description=description,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "home",
            "description": "default functions"
        },
        {
            "name" : "questions",
            "description": "functions that are used to get the questionnary"
        },
        {
            "name": "admin",
            "description": "functions for the admin to add a question"
        },
        {
            "name": "auth",
            "description": "function to get the token"
        }
    ]
)


# Get all the routers
app.include_router(user.ques, dependencies=[Depends(security.get_current_user)])
app.include_router(admin.admin, dependencies=[Depends(security.get_current_role_user)])
app.include_router(security.auth)


@app.get("/home", tags=["home"], name="Status of the API")
async def get_api_status():
    """Return a message if the API is working."""
    return {"status": "the API works"}

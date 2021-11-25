# exam-fastapi

My first api

## Instruction to launch the API

### To launch the API server from a virtual environment, follow the steps following :  

- From the project directory, create the virtual environment :  
`python3 -m venv <venv>`  
- Activate the virtual environment :  
    * On Linux :  
    `$ source <venv> / bin / activate`  
    * On Windows Powershell :  
    `PS C: \<venv>\Scripts\Activate`  
-  Install the necessary modules :  
`pip install –r requirements.txt` or `pip3 install –r requirements.txt`  
- Start the server from the folder app :  
`uvicorn api: app`  
- Check the operating status of the API :  
`curl -X 'GET' 'http://localhost:8000/home' -H 'accept: application/json'`  

## Creation of a questionnaire (authentication required)  

- Token request to authenticate :  
`curl -X 'POST' 'http://localhost:8000/token' \`  
`-H 'accept: application/json' \`  
`-H 'Content-Type: application/x-www-form-urlencoded' \`  
`-d  'grant_type=&username=<username>&password=<password>&scope=&client_id=&client_secret='`  
- Request the types of tests available :  
`curl -X 'GET' 'http://localhost:8000/uses' \`  
`-H 'accept: application/json' \`  
`-H 'Authorization: Bearer <token>'`  
- Ask the subjects according to the type of test chosen :  
`curl -X 'GET' 'http://localhost:8000/subjects?use=<type de test>' \`  
`-H 'accept: application/json' \`  
`-H 'Authorization: Bearer <token>'`  
- Ask for a questionnaire :  
`curl -X 'GET' 'http://localhost:8000/questions?nb_questions=<number>&subject=<subject>&use=<test type>' \`  
`-H 'accept: application/json' \`  
`-H 'Authorization: Bearer <token>'`  

## Adding a question to the database (authentication required with admin rights)  

- Token request to authenticate with role admin :  
`curl -X 'POST' 'http://localhost:8000/token' \`  
`-H 'accept: application/json' \`  
`-H 'Content-Type: application/x-www-form-urlencoded' \`  
`-d  'grant_type=&username=<username>&password=<password>&scope=admin&client_id=&client_secret='`  
- Add a question in the database :  
`curl -X 'POST' 'http://localhost:8000/admin' \`  
`-H 'accept: application/json' \`  
`-H 'Authorization: Bearer <token> ' \`  
`-H 'Content-Type: application/json' \`  
`-d '{`  
`"question": "string",`  
`"subject": "string",`  
`"use": "string",`  
`"correct": "string",` 
`"responseA": "string",`  
`"responseB": "string",`  
`"responseC": "string",`  
`"responseD": "string",`  
`"remark": "string"`  
`}'`  

## Documentation  

Documentation in OpenAPI format can be accessed at :  
http://localhost:8000/docs

## Author  
Nicolas MARQUETTE
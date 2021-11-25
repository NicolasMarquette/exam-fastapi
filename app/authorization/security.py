"""Security and authorization management"""

from fastapi import Depends, HTTPException, status, APIRouter, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from schemas import user_schema, token_schema
from authorization.config import settings
from db import db_users


# Import the fake users database.
users_db = db_users.users

# Utility function to Hash.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility function to authenticate.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"admin": "Administrator rights"}
)

auth = APIRouter()


def verify_password(plain_password, hashed_password):
    """Verify if the password received match the hashed_password in database.
    
    Parameters
    ----------
    plain_password : str
        The password received from the authentication form.
    hashed_password : str
        The hashed password stored in the database.
    
    Return
    ------
    bool : The resultat of the verification.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash the password received.
    
    Parameter
    ---------
    password : str
        The password received from the authentication form.
    
    Return
    ------
    str : The password hashed.
    """
    return pwd_context.hash(password)


def get_user(db, username: str):
    """Get the users data from the database.
    
    Parameters
    ----------
    db : dict        
        A database in dict format.
    username : str
        The user username. 

    Return
    ------
    UserInDB : The user's data for the specified username. 
    """
    if username in db:
        user_dict = db[username]
        return user_schema.UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    """Authenticate the user by checking if their username exists 
    and if the password matches. 
    
    Parameters
    ----------
    db : dict        
        A database in dict format.
    username : str
        The user username. 
    password : str
        The user password.

    Return
    ------
    user : UserInDB : The user's data for the specified username.    
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    """Create an access token to authenticate.
    
    Parameter
    ---------
    data : dict
        The data with the entered username and scope.
    
    Return
    ------
    encode_jwt : str
        The data encoded to create a token.
    """
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    """Get the current user after verifying the token.
    
    Parameters
    ----------
    security_scopes : SecurityScopes
        To get the scopes object.
    token : str
        The token that was created for the user.
    
    Raises
    ------
    HTTPException : 401 
        Could not validate credentials if token decoding fails,
        the data is not valid with the model or there is no username.
    HTTPException : 401
        Not enough permissions if attempting to access an endpoint 
        without the correct authorization.
    
    Return
    ------
    user : UserInDB : The user's data for the specified username.
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token received.
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Get the username in the token.
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Get the scope in the token.
        token_scopes = payload.get("scopes", [])
        token_data = token_schema.TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    # Get the user's data from the username in the token.
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        # Verify if the scope from the scopes list is in the token.
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value}
            )
    return user


async def get_current_role_user(
    current_user: user_schema.User = Security(get_current_user, scopes=["admin"])
):
    """Verify if the access according to the user's role.
    
    Parameter
    ---------
    current_user : UserInDB
        The user's data for the specified username.
    
    Raise
    -----
    HTTPException : 401
        Not authorized if the user does not have the admin role.
    
    Return
    ------
    current_user : UserInDB
        The user's data for the specified username.
    """
    if not current_user.role == "admin":
        raise HTTPException(status_code=401, detail="Not authorized")
    return current_user


@auth.post("/token", response_model=token_schema.Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Give a token for the authorization.
    \f
    Parameter
    ---------
    form_data : OAuth2PasswordRequestForm
        The authorization request form.
    
    Raise
    -----
    HTTPException : 401
        Incorrect username or password if the username or the password input is not correct.
    
    Return
    ------
    dict : A dictionnary with the token and the type of token.    
    """
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes}
    )
    return {"access_token": access_token, "token_type": "bearer"}

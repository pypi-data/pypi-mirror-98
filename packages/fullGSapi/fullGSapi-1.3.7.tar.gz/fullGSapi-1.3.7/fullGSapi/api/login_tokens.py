import pathlib
import pickle
import pytz
import getpass

from datetime import datetime
from dateutil.parser import parse

from .client import GradescopeClient
from .gs_api_client import GradescopeAPIClient

DEFAULT_TOKEN_PATH = "~/.gradescope"
TOKEN_VERSION = "1.0.0"

class LoginTokens:
    def __init__(self, email: str=None, gsAPI: GradescopeAPIClient=None, gsFullapi: GradescopeClient=None, path: str=DEFAULT_TOKEN_PATH):
        self.token_version = TOKEN_VERSION
        self.email = email
        self.gsAPI = gsAPI
        self.gsFullapi = gsFullapi
        self.path = path

    def save(self, path: str=None):
        if path is None:
            path = self.path
        p = pathlib.Path(path).expanduser().absolute()
        p.parent.mkdir(0o600, parents=True, exist_ok=True)
        with open(p, "wb+") as f:
            pickle.dump(self, f)
        
    @staticmethod
    def load(path: str=None) -> "LoginTokens":
        if path is None:
            path = DEFAULT_TOKEN_PATH
        if pathlib.Path(path).expanduser().absolute().exists():
            print("Found token file! Verifying login...")
            token: LoginTokens = LoginTokens._load(path)
            if token.is_logged_in():
                return token
        else:
            print(f"Could not find the token '{path}'")

    @staticmethod
    def _load(path: str) -> "LoginTokens":
        if path is None:
            path = DEFAULT_TOKEN_PATH
        with open(pathlib.Path(path).expanduser().absolute(), "rb") as f:
            return pickle.load(f)

    def is_logged_in(self) -> bool:
        if self.gsAPI is None or self.gsFullapi is None:
            print("You are not logged in!")
            return False
        api_expiration = self.gsAPI.cookie.get("token_expiration_time")
        logged_in = api_expiration and parse(api_expiration) > datetime.now(pytz.UTC) and self.gsFullapi.verify_logged_in()
        if logged_in:
            print(f"Logged in with {self.email}!")
            return True
        else:
            print("You are not logged in!")
            return False

    def login(self, email: str, password: str) -> bool:
        if self.gsAPI is None:
            self.gsAPI = GradescopeAPIClient()
        if self.gsAPI.log_in(email, password):
            if self.gsFullapi is None:
                self.gsFullapi = GradescopeClient()
            if self.gsFullapi.log_in(email, password):
                print(f"Login Successful for {email}!")
                self.email = email
                self.save()
                return True
            else:
                print("Failed to login to the frontend API!")
        else:
            print("Failed to login to the official API!")
        return False

    def prompt_login(self, force: bool=False, until_success: bool=True, email=None):
        logged_in = not force and self.is_logged_in()
        gs_email_str = "Gradescope Email: "
        while not logged_in:
            if email is None:
                gsemail = input(gs_email_str)
            else:
                print("Gradescope Email: " + email)
                gsemail = email
            password = getpass.getpass("Gradescope Password: ")
            logged_in = self.login(gsemail, password)

        return self
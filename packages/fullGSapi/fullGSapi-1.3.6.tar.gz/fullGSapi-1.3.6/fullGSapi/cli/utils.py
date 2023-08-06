import click
import os
import pathlib
import pickle
import pytz

from datetime import datetime
from dateutil.parser import parse

from fullGSapi.api.login_tokens import LoginTokens

login_token_path_option = click.option(
    "--token", "-t", "tokenpath", default="~/.gradescope", help="The path to the token file.", type=click.Path()
)

course_id_option = click.option(
    "--course", "-c", "course", prompt=True, help="This is the Gradescope Course ID.", type=str
)
assignment_id_option = click.option(
    "--assignment", "-a", "assignment", prompt=True, help="This is the Gradescope Assignment ID.", type=str
)

submission_id_option = click.option(
    "--submission", "-s", "submission", prompt=True, help="This is the Gradescope Submission ID.", type=str
)

def get_clients(ctx, path: str, do_login_on_fail: bool=True) -> LoginTokens:
    token: LoginTokens = LoginTokens.load(path)
    if token:
        return token
    print("If you would like to login, please follow the prompts.")
    if not do_login_on_fail:
        return False
    lt = None
    from fullGSapi.cli.login import login
    while not lt:
        email = click.prompt("Email", type=str)
        password = click.prompt("Password", hide_input=True, type=str)
        lt = ctx.invoke(login, email=email, password=password, tokenpath=path)
    return lt
    
def get_tokens(ctx):
    ctx.obj["TOKEN"] = get_clients(ctx, ctx.obj["TOKENPATH"])
    return ctx.obj["TOKEN"]

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    if os.path.isfile(dirName):
        return [dirName]
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles
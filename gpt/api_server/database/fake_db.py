from typing import List
from pydantic import BaseModel, parse_file_as
from api_server import helper
from api_server.database.class_loader import User, ClassLoader


class userRepo:
    def __init__(self):
        self.users: List[User] = []

    def getUser(self):
        return self.users

    def InitData(self):
        print(helper.data_file)
        master_data: ClassLoader = parse_file_as(path=helper.data_file, type_=ClassLoader)
        self.users = master_data.user
        print("================")
        print(master_data.user)
        return self

    def getRootUser(self):
        return self.users[0]


class FakeDB:
    def __init__(self):
        self.repo: userRepo = userRepo().InitData()

    def getUserRepo(self):
        return self.repo

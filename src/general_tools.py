#This modules contains general tools which can be reused anytime

##########
#Libraries
##########
import inspect
import json

DEV=False
#To uncomment during testing phase
#DEV=True

########
#Classes
########
#Mock Response in json with a status code to determine
class MockResponse:
    def __init__(self, json_file, status):
        with open(json_file, 'r') as f:
            self.data = json.load(f)
        self.status_code = status
    
    def json(self):
        return self.data




###################
# Errors management
###################
def err_management():
    print(f"Error in :\n  - File: {inspect.currentframe().f_back.f_code.co_filename}\n  - Function: {inspect.currentframe().f_back.f_code.co_name}")

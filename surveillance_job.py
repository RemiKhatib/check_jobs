#The role of this job is to select all the jobs which could interest me among a list of websites
#Plan :
# 1) Define the list of websites. Create the rules to respect during the search. At each run, it should avoid duplicates.
# 2) Store everything in a database. The table should contain : date of execution, title of the job, adress, description.
# 3) Check Beautiful Soup to go though websites
# 4) Check for the API of the websites
# 5) Make one module per website
# 6) Create a database
# 7) Make the python requierements.txt "pip freeze > requirements.txt"

##########
#Libraries
##########
from BPCE import *


##########################
#Loop through the websites
##########################
bpce_read()

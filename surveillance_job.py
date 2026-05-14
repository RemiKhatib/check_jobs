##########
#Libraries
##########
from BPCE import *


##########################
#Loop through the websites
##########################
jobs=bpce_read()
for job in jobs :
    print(f"{job["website"]} ; {job["id"]} ; {job["title"]} ; {job["city"]} ; {job["date_creation"]} ; {job["date_found"]}")

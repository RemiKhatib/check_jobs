##########
#Libraries
##########
import BPCE
import table
#import csv
import tabulate

#####################
# Initialize database
#####################
db = table.DatabaseManager()
db.create_table()


##########################
#Loop through the websites
##########################
jobs=BPCE.bpce_read()
db.upsert(jobs)


################################
#Store the result in a html file
################################
filename="job_offers.html"
#print(db.select_all()[0])
with open(filename, 'w') as f:
    f.write(tabulate.tabulate(
        db.select_all(),
        headers=("website", "id", "title", "company", "link", "description", "city", "zipcode", "address", "date_creation", "date_found", "date_applied"),
        tablefmt="unsafehtml"))


###################
#Closing everything
###################
db.close()

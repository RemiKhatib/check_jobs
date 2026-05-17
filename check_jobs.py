##########
#Libraries
##########
import BPCE
import BdF
import APEC
import table
import tabulate
import logging

logger = logging.getLogger(__name__)

###########
# Constants
###########
SOURCES = [BPCE, BdF, APEC]
OUTPUT_FILE = "job_offers.html"
HEADERS = ("Website", "Id", "Company", "Title", "City", "Zipcode", 
           "Date of creation", "Date found", "Checked", "To apply", "Application date")


#####################
# Initialize database
#####################
db = table.DatabaseManager()
db.create_table()


##########################
#Loop through the websites
##########################
for source in SOURCES:
    try :
        jobs = source.read()
        db.upsert(jobs)
    except Exception as e:
        logger.error(f"Scraping error {source.__name__}: {e}")


################################
#Store the result in a html file
################################
#print(db.select_all()[0])
with open(OUTPUT_FILE, 'w') as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n<style>\ntable, th, td {\n  border: 1px solid black;\n  border-collapse: collapse;\n}\n</style>\n</head>\n<body>\n\n<h1>To check</h1>\n")
    f.write(tabulate.tabulate(
        db.select_to_check(),
        headers=HEADERS,
        tablefmt="unsafehtml"))
    f.write("\n\n<h1>Applied</h1>\n")
    f.write(tabulate.tabulate(
        db.select_applied(),
        headers=HEADERS,
        tablefmt="unsafehtml"))
    f.write("\n\n</body>\n</html>\n")

###################
#Closing everything
###################
db.close()

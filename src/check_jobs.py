##########
#Libraries
##########
from config import *

from . import apec
from . import bdf
from . import bpce
from . import table

import logging
import tabulate


def main():
    SOURCES = [apec, bdf, bpce]                     # List of scrappers
    logger = logging.getLogger(__name__)


    #####################
    # Initialize database
    #####################
    db = table.DatabaseManager(str(DATABASE_FILE))
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
    output_path = OUTPUT_DIR / HTML_FILE
    with open(output_path, 'w') as f:
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



if __name__=="__main__":
    main()

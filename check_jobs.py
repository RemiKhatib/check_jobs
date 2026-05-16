##########
#Libraries
##########
import BPCE
import table
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
    f.write("<!DOCTYPE html>\n<html>\n<head>\n<style>\ntable, th, td {\n  border: 1px solid black;\n  border-collapse: collapse;\n}\n</style>\n</head>\n<body>\n\n<h1>To check</h1>\n")
    f.write(tabulate.tabulate(
        db.select_to_check(),
        headers=("Website", "Id", "Company", "Title", "City", "Zipcode", "Date of creation", "Date found", "Checked", "To apply", "Application date"),
        tablefmt="unsafehtml"))
    f.write("\n\n<h1>Applied</h1>\n")
    f.write(tabulate.tabulate(
        db.select_applied(),
        headers=("Website", "Id", "Company", "Title", "City", "Zipcode", "Date of creation", "Date found", "Checked", "To apply", "Application date"),
        tablefmt="unsafehtml"))
    f.write("\n\n</body>\n</html>\n")

###################
#Closing everything
###################
db.close()

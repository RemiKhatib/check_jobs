import pathlib as pl

DEV=True
#To uncomment during testing phase
#DEV=True


###########
# Constants
###########
HEADERS = ("Website", "Id", "Company", "Title", "City", "Zipcode", 
        "Date of creation", "Date found", "Checked", "To apply", "Application date")  # Header for the tables
NB_OFFERS_MAX=total=500      #Number maximal of offers displayed by the API



#######################
# Directories and files
#######################
PROJECT_ROOT = pl.Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"            # Output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
HTML_FILE= "job_offers.html"                    # Output file (HTML with databases)
DATABASE_FILE= OUTPUT_DIR / "database.db"       # Database with the different job offers and their state



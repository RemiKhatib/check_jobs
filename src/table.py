#Module with everything about database

##########
#Libraries
##########
import config
from . import general_tools as gt

import sqlite3

#Class for the access to the table listing the job offers
class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
        
    def close(self):
        self.con.close()


    ########################################
    #Create a table if it does not exist.abs   
    ########################################
    # - id_prim       : Primary index
    # - website       : Website where I found it
    # - id            : Id of the job on the website
    # - company       : Company who proposes the job
    # - title         : title of the job
    # - link          : link to the offer
    # - city          : city of the job
    # - zipcode       : zip code of the city
    # - address       : adress (street, ...)
    # - date_creation : date when the offer was posted
    # - date_found    : date when the offer has been recorded on the DB
    # - checked       : To check if I saw the offer
    # - to_apply      : To analyse more carefully and decide if I have to apply
    # - date_applied  : Application date
    # - last_update   : Last update of the record
    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS job_offers (
                id_prim         INTEGER PRIMARY KEY AUTOINCREMENT,
                website         TEXT NOT NULL,
                id              TEXT NOT NULL,
                company         TEXT DEFAULT NULL,
                title           TEXT DEFAULT NULL,
                link            TEXT DEFAULT NULL,
                city            TEXT DEFAULT NULL,
                zipcode         INTEGER DEFAULT NULL,
                address         TEXT DEFAULT NULL,
                date_creation   DATE DEFAULT NULL,
                date_found      DATE DEFAULT NULL,
                checked         INTEGER DEFAULT 0,
                to_apply        INTEGER DEFAULT 0,
                date_applied    DATE DEFAULT NULL,
                last_update     DATE DEFAULT NULL,
                UNIQUE(website, id)
            )
        """)
        self.con.commit()




    #Upsert a list of dict
    def upsert(self, ldict):
        nb_ok=0
        try :
            for job in ldict:
                for key, value in job.items():
                    if isinstance(value, list):
                        print(f"ERROR: {key} is a list: {value}")
                try:
                    #We insert everything but checked, to_apply and date_applied
                    #We update everything we inserted but date_found
                    self.cur.execute("""
                        INSERT INTO job_offers (website, id, company, title, link, city, zipcode, address, date_creation, date_found, last_update)
                        VALUES (:website, :id, :company, :title, :link, :city, :zipcode, :address, :date_creation, :date_found, :last_update)
                        ON CONFLICT(website, id) DO UPDATE SET
                            company         = excluded.company      ,
                            title           = excluded.title        ,
                            link            = excluded.link         ,
                            city            = excluded.city         ,
                            zipcode         = excluded.zipcode      ,
                            address         = excluded.address      ,
                            date_creation   = excluded.date_creation,
                            last_update     = excluded.last_update
                    """, job)
                    nb_ok+=1
                except sqlite3.IntegrityError as e:
                    print(f"Error upserting record {job['website']}, {job['id']}: {e}")
            self.con.commit()
            print(f"{ldict[0]["website"]}: Processed {nb_ok}/{len(ldict)} records.")
        except Exception as e:
            self.con.rollback()
            gt.err_management()
            print(f"Unexpected error: {e}\nRollback for {ldict[0]["website"]} offers.")


    #Display all the jobs that I have to yet checked or the jobs where I should apply.
    #All the columns are displayed but primary key, address and last_update.
    # I associate "title" and "link" in the same column.
    def select_to_check(self):
        self.cur.execute("""
            SELECT 
                website,
                id,
                company,
                concat('<a href="',link,'" target="_blank">',title,'</a>'),
                city,
                zipcode,
                date_creation,
                date_found,
                checked,
                to_apply,
                date_applied
            FROM job_offers
            WHERE (checked=0 OR (to_apply<>0 AND date_applied is null))
            order by date_creation, date_found
        """)
        return self.cur.fetchall()


    #Display all the jobs where I applied
    #All the columns are displayed but primary key, address and last_update.
    # I associate "title" and "link" in the same column.
    def select_applied(self):
        self.cur.execute("""
            SELECT 
                website,
                id,
                company,
                concat('<a href="',link,'" target="_blank">',title,'</a>'),
                city,
                zipcode,
                date_creation,
                date_found,
                checked,
                to_apply,
                date_applied
            FROM job_offers
            WHERE date_applied is not null
            order by date_applied desc, date_creation desc
        """)
        return self.cur.fetchall()

    #Delete old data:
    #  - job_offers where I did not apply and not appearing for 1 month
    #  - job_offers where I applied but not appearing for 1 year
    def delete_old(self):
        self.cur.execute(f"""
            DELETE
            FROM job_offers
            WHERE (last_update < date('now','-{config.MONTHS_NOT_APPLIED} month') and date_applied is null)
               OR  last_update < date('now','-{config.YEARS_APPLIED} year')
        """)
        self.con.commit()
        print(f"{self.cur.rowcount} job offers deleted")



if __name__ == "__main__":
    print("Test the DatabaseManager class (only select)")
    
    db = DatabaseManager()
  
    print("\nTest: select_to_check")
    print(db.select_to_check())
    
    print("\n\nTest: select_applied")
    print(db.select_applied())
    
    db.close()
    print("\n\nAll tests completed successfully")


    
    

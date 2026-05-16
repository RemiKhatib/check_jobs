#Module with everything about database

import sqlite3
import general_tools as gt

#Class for the access to the table listing the job offers
class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    #Create a table if it does not exist    
    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS job_offers (
                id_prim         INTEGER PRIMARY KEY AUTOINCREMENT,
                website         TEXT NOT NULL,
                id              TEXT NOT NULL,
                title           TEXT DEFAULT NULL,
                company         TEXT DEFAULT NULL,
                link            TEXT DEFAULT NULL,
                description     TEXT DEFAULT NULL,
                city            TEXT DEFAULT NULL,
                zipcode         INTEGER DEFAULT NULL,
                address         TEXT DEFAULT NULL,
                date_creation   DATE DEFAULT NULL,
                date_found      DATE DEFAULT NULL,
                date_applied    DATE DEFAULT NULL,
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
                    #We insert everything but the date of application.
                    #We update everything but the date of application and the date when it has been found
                    self.cur.execute("""
                        INSERT INTO job_offers (website, id, title, company, link, description, city, zipcode, address, date_creation, date_found)
                        VALUES (:website, :id, :title, :company, :link, :description, :city, :zipcode, :address, :date_creation, :date_found)
                        ON CONFLICT(website, id) DO UPDATE SET
                            title           = excluded.title        ,
                            company         = excluded.company      ,
                            link            = excluded.link         ,
                            description     = excluded.description  ,
                            city            = excluded.city         ,
                            zipcode         = excluded.zipcode      ,
                            address         = excluded.address      ,
                            date_creation   = excluded.date_creation
                    """, job)
                    nb_ok+=1
                except sqlite3.IntegrityError as e:
                    print(f"Error upserting record {job['website']}, {job['id']}: {e}")
            self.con.commit()
            print(f"Processed {nb_ok}/{len(ldict)} records.")
        except Exception as e:
            self.con.rollback()
            gt.err_management()
            print(f"Unexpected error: {e}\nRollback for {ldict[0]["website"]} offers.")


    #Display everything but primary key
    def select_all(self):
        self.cur.execute("""
            SELECT website, id, title, company, link, description, city, zipcode, address, date_creation, date_found, date_applied
            FROM job_offers 
            order by date_creation desc, date_applied desc
        """)
        return self.cur.fetchall()



    def close(self):
        self.con.close()


    
    

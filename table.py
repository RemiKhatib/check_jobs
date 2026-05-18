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
                        INSERT INTO job_offers (website, id, company, title, link, city, zipcode, address, date_creation, date_found)
                        VALUES (:website, :id, :company, :title, :link, :city, :zipcode, :address, :date_creation, :date_found)
                        ON CONFLICT(website, id) DO UPDATE SET
                            company         = excluded.company      ,
                            title           = excluded.title        ,
                            link            = excluded.link         ,
                            city            = excluded.city         ,
                            zipcode         = excluded.zipcode      ,
                            address         = excluded.address      ,
                            date_creation   = excluded.date_creation
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
    #All the columns are displayed but primary key and address. Associate "title" and "link" in the same column.
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
    #All the columns are displayed but primary key and address. Associate "title" and "link" in the same column.
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



    def close(self):
        self.con.close()


if __name__ == "__main__":
    print("Test the DatabaseManager class (only select)")
    
    db = DatabaseManager()
  
    print("\nTest: select_to_check")
    print(db.select_to_check())
    
    print("\n\nTest: select_applied")
    print(db.select_applied())
    
    db.close()
    print("\n\nAll tests completed successfully")


    
    

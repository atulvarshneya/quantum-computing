import sqlite3
from typing import List, Tuple, Any, Optional
import os


class JobsDB:
    """Database manager for storing and retrieving jobs data."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the JobsDB.
        
        Args:
            db_path: Path to the SQLite database file. If None, defaults to '~/jobs.db'.
        """
        self.db_path = db_path or os.path.expanduser('~/jobs.db')
        self.conn = None
        self.cur = None

    def __enter__(self):
        """Connect to the database when entering context."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()
            return self
        except sqlite3.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Commit changes and close connection when exiting context."""
        if self.conn:
            if exc_type is None:
                try:
                    self.conn.commit()
                except sqlite3.Error as e:
                    print(f"Error committing changes: {e}")
            self.conn.close()

    def create_db_table(self) -> None:
        """Create jobs table if it doesn't exist."""
        try:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    jobid INTEGER PRIMARY KEY AUTOINCREMENT, 
                    job_request BLOB, 
                    job_result BLOB
                )
            """)
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to create table: {e}")

    def insert_request(self, job_request: Any) -> int:
        """Insert a new job request and return its ID.
        
        Args:
            job_request: The job request data to store
            
        Returns:
            The newly created job ID
        """
        try:
            cursor = self.conn.execute(
                """INSERT INTO jobs (job_request) VALUES (?)""", 
                (job_request,)
            )
            return cursor.lastrowid
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to insert request: {e}")

    def update_job_result(self, jobid: int, job_result: Any) -> None:
        """Update the result for a specific job.
        
        Args:
            jobid: The job ID to update
            job_result: The result data to store
        """
        try:
            self.conn.execute(
                """UPDATE jobs SET job_result=? WHERE jobid=?""", 
                (job_result, jobid)
            )
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to update job result: {e}")

    def fetch_request_by_jobid(self, jobid: int) -> List[Tuple]:
        """Fetch a job by its ID.
        
        Args:
            jobid: The job ID to fetch
            
        Returns:
            List of job data tuples matching the ID
        """
        try:
            cur = self.conn.execute(
                """SELECT * FROM jobs WHERE jobid=?""", 
                (jobid,)
            )
            return cur.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to fetch job with ID {jobid}: {e}")

    def fetch_requests_all(self) -> List[Tuple]:
        """Fetch all jobs from the database.
        
        Returns:
            List of all job data tuples
        """
        try:
            cur = self.conn.execute("""SELECT * FROM jobs""")
            return cur.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to fetch all jobs: {e}")

    def remove_request_by_jobid(self, jobid: int) -> None:
        """Remove a job by its ID.
        
        Args:
            jobid: The job ID to remove
        """
        try:
            self.conn.execute(
                """DELETE FROM jobs WHERE jobid=?""", 
                (jobid,)
            )
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to delete job with ID {jobid}: {e}")

    def update_request_by_jobid(self, jobid: int, job_request: Any) -> None:
        """Update a job request by its ID.
        
        Args:
            jobid: The job ID to update
            job_request: The new job request data
        """
        try:
            self.conn.execute(
                """UPDATE jobs SET job_request=? WHERE jobid=?""", 
                (job_request, jobid)
            )
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to update job with ID {jobid}: {e}")

    def get_database_schema(self) -> List[Tuple]:
        """Get the database schema information.
        
        Returns:
            Database schema details
        """
        try:
            cur = self.conn.execute("SELECT * FROM sqlite_master;")
            return cur.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to fetch database schema: {e}")


if __name__ == '__main__':
    try:
        with JobsDB() as jdb:
            jdb.create_db_table()
            
            # Insert and retrieve a job
            job_id = jdb.insert_request('sample job request')
            print(f"Inserted job with ID: {job_id}")
            
            # Update with a result
            jdb.update_job_result(job_id, 'sample job result')
            
            # Fetch the job
            job = jdb.fetch_request_by_jobid(job_id)
            print(f"Retrieved job: {job}")
            
            # Fetch all jobs
            all_jobs = jdb.fetch_requests_all()
            print(f"All jobs count: {len(all_jobs)}")
            
            # Get schema
            schema = jdb.get_database_schema()
            print(f"Database schema: {schema}")
    except Exception as e:
        print(f"Error: {e}")

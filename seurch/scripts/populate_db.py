from insig.db.pgsql.sql_client import SQLClient
from insig.logging.logger import Logger
import re

logger = Logger().get_logger()

class PopulateDb:
    S3_BUCKET = "s3://filingdb.lazard.live.v.2.0.6.1"
    REPORT_TYPES = {"a": "Annual",
                    "i": "Interim",
                    "ea": "Annual (Extended)",
                    "ei": "Interim (Extended)"}

    def populate(self):
        input_file = "../../lazard_list.tsv"
        with open(input_file, "r") as s3_file:
            entries = s3_file.readlines()

        entries = self.get_distinct_entries(entries)
        logger.info(f"got {len(entries)} distinct entries")
        self.insert_entries(entries)

    def get_distinct_entries(self, entries):
        distinct_entries = []

        for entry in entries:
            if "file.pdf" in entry:
                distinct_entries.append(entry)

        return distinct_entries

    def insert_entries(self, entries):
        counter = 0
        for entry in entries:
            row = self.setup_row(entry)
            self.insert_row(row, counter)

    def setup_row(self, entry):
        entry = re.sub(" +", " ", entry)
        s3_date, s3_time, size, s3_path = entry.split()
        s3_path_components = s3_path.split("/")
        report_type = self.REPORT_TYPES[s3_path_components[0]]
        s3_prefix = "/".join(s3_path_components[0:4])
        s3_key = s3_path_components[2]

        s3_create_time = f"{s3_date} {s3_time}"
        return [self.S3_BUCKET, s3_prefix, s3_key, s3_create_time, report_type]

    def insert_row(self, row, counter):
        client = self.get_sql_client()
        query = "INSERT INTO documents (s3_bucket, s3_path, s3_key, s3_create_date, report_type)"
        query += " VALUES(%s, %s, %s, %s, %s)"

        client.run_insert(query, row)
        counter += 1
        if counter % 100 == 0:
            logger.info(f"inserted 100")

    def get_sql_client(self):
        config = { "user": "root", "password": "r00t66", "host": "localhost", "port": 5432, "database": "seurch_dev"}
        client = SQLClient(config)
        return client


if __name__ == "__main__":
    PopulateDb().populate()
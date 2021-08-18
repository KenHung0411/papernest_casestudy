
from ftplib import FTP
from io import BytesIO
import os
import pandas as pd

class ftpService:
    def __init__(self, username, password, host_name):
        self.username = username
        self.password = password
        self.host_name = host_name

    def connect_ftp_service(self):
        ftp =  FTP(self.host_name)
        ftp.login(self.username, self.password)
        return ftp

    def read_file_with_df(self):
        ftp = self.connect_ftp_service()
        ftp.cwd('files')
        r = BytesIO()
        ftp.retrbinary('RETR raw_calls.csv', r.write)
        r.seek(0)
        df = pd.read_csv(r, header=0)
        df = df.dropna(how="all")
        df = df.astype({"id": int, 
                        "called_number": str,
                        "date":str,
                        "duration_in_sec":int,
                        "incoming_number":str})
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
        df["incoming_number"] = df["incoming_number"].apply(lambda a: a.replace(".0", ""))
        df["incoming_number"] = df["incoming_number"].apply(lambda a: "0" + a)
        return df


if __name__ == "__main__":
    user_name = os.environ["FTP_USER_NAME"]
    password = os.environ["FTP_PASSWORD"]
    host_name = os.environ["FTP_HOST_NAME"]

    ftp_service = ftpService(user_name, password, host_name)
    df = ftp_service.read_file_with_df()
    print(df.head())
from dbService import dbService
from ftpService import ftpService
from mail import EmailService
import pandas as pd
import os

def transoform():

    user_name = os.environ["USER_NAME"]
    password = os.environ["PASSWORD"]
    host_name = os.environ["HOST_NAME"]
    db_name = os.environ["DB_NAME"]

    db_service = dbService(user_name, password, host_name, db_name)
    df_postgres = db_service.read_table_through_df()


    user_name = os.environ["FTP_USER_NAME"]
    password = os.environ["FTP_PASSWORD"]
    host_name = os.environ["FTP_HOST_NAME"]

    ftp_service = ftpService(user_name, password, host_name)
    df_ftp = ftp_service.read_file_with_df()

    ## Merging step
    df_merge = df_ftp.merge(df_postgres, how="left", left_on='incoming_number', right_on='PhoneNumber')
    df_merge = df_merge.rename(columns={"id_x": "client_id", "id_y": "call_id", "date": "call_date"})
    df_merge["full_name"] = df_merge["FirstName"] + " " + df_merge["LastName"]
    select_columns = ["client_id", "FirstName", "full_name", "LastName", "PhoneNumber", "call_date", "duration_in_sec"]
    df_merge = df_merge[select_columns]


    ## Group by step for average of druation
    df_groupby_avg = df_merge.groupby(['full_name']).mean()[["duration_in_sec"]].reset_index()
    df_groupby_avg = df_groupby_avg.rename(columns={"duration_in_sec": "avg_duration_in_sec"})

    ## Group by step for first call date
    df_groupby_first = df_merge.groupby(['full_name']).first()[["call_date"]].reset_index()
    df_groupby_first = df_groupby_first.rename(columns={"call_date": "first_call_date"})


    ## Merging grouped table back to the main table
    df_f_merge = df_merge.merge(df_groupby_avg, how="left", on="full_name")
    df_f_merge = df_f_merge.merge(df_groupby_first, how='left', on="full_name")


    # final write file
    select_columns = ["client_id", "FirstName", "LastName", "PhoneNumber", "first_call_date", "avg_duration_in_sec"]
    df_f_merge = df_f_merge.dropna(how="any")
    client_list = list(df_f_merge["full_name"])
    df_f_merge = df_f_merge[select_columns]
    df_f_merge.to_csv('./output/result.csv', index = False)

    return client_list

    

if __name__ == "__main__":

    client_list = transoform()


    mail_password = os.environ["MAIL_PWD"]
    mail_sender = os.environ["MAIL_SENDER"]
    mail_receiver = os.environ["MAIL_RECEIVER"]

    mail_service= EmailService(mail_sender, mail_password, mail_receiver, client_list)
    mail_service.send_mail()


   


    








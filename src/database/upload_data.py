import json
import sys
import os
import configparser
import pymongo
import process_data 

"""
this file is ran as py upload_data.py config.ini
(or whatever you'd like to call it)
"""

def test_process():
    streams = process_data.getStreamsAll()
    print(f"Length of streams: {len(streams)}")
    filtered_streams = process_data.getStreamsFiltered(25)
    print(f"Length of filtered streams: {len(filtered_streams)}")

def main():

    print("Uploading data...")

    config_file = sys.argv[1]

    #access .ini config file to get connection string and database name (you set these yourself!)
    config = configparser.ConfigParser()
    config.read(config_file)
    connection_string = config['database']['connection_string']
    database_name = config['database']['database_name']



    print(len(requesting))

if __name__ == "__main__":
    main()
import json
import sys
import os
import configparser
import pymongo
from pymongo import MongoClient
import streams as streamobj
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

def prepare_streams(filename):
    #converts json array to list of pymongo InsertOne operations

    requesting = []

    with open(filename, "r") as f:
        try:
            # Load the entire JSON array
            data = json.load(f)  # Use json.load() instead of json.loads() for a file object
            
            # Check if the data is a list
            if isinstance(data, list):
                for obj in data:
                    # Add each object in the array to the list of InsertOne operations
                    requesting.append(InsertOne(obj))
            else:
                print("The JSON file does not contain a list at the top level.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return requesting

def convert_streams(streams):

    stream_objs = []

    for s in streams:
        obj = streamobj.Stream(s['ts'], s['platform'], s['ms_played'], s['conn_country'],
                             s['master_metadata_track_name'],
                             s['master_metadata_album_artist_name'],
                             s['master_metadata_album_album_name'],
                             s['spotify_track_uri'], s['reason_start'], s['reason_end'],
                             s['shuffle'], s['skipped'], s['offline'])
        stream_objs.append(obj)

    stream_dicts = []

    for obj in stream_objs:
        stream = obj.to_dict()
        stream_dicts.append(stream)

    return stream_dicts

def main():

    print("Uploading data...")

    #access dbinfo.ini config file to get connection string and database name (you set these yourself!)
    config = configparser.ConfigParser()
    config.read('dbinfo.ini')
    connection_string = config['database']['connection_string']
    database_name = config['database']['database_name']

    streams = process_data.getStreamsFiltered(25) #gets any stream over 25 seconds
    db_streams = convert_streams(streams) #convert to the format I want for the database

    client = MongoClient(connection_string)
    db = client[database_name]
    stream_collection = db["streams"] 

    



if __name__ == "__main__":
    main()
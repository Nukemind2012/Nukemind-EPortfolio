#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Connection Variables
        USER = 'aacuser'
        PASS = 'SNUH1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 33894
        DB = 'AAC'
        COL = 'animals'

        # Initialize Connection
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

        # Create method- the C in Crud
    def create(self, data):
        if data is not None:
            try:
                result = self.collection.insert_one(data)
                print('Inserted document ID:', result.inserted_id)
                return True
            except Exception as e:
                print('Insert failed:', e)
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Read method- the R in cRud
    def read(self, query):
        if query is not None:
            try:
                result = list(self.collection.find(query))
                return result
            except Exception as e:
                print('Read failed:', e)
                return []
        else:
            return []

    # Update method- the U in crUd
    def update(self, query, update_data):
        if query is not None and update_data is not None:
            try:
                result = self.collection.update_many(query, {"$set": update_data})
                print('Documents modified:', result.modified_count)
                return result.modified_count
            except Exception as e:
                print('Update failed:', e)
                return 0
        else:
            raise Exception("Query and update_data cannot be None")

    # Delete method- the D in cruD
    def delete(self, query):
        if query is not None:
            try:
                result = self.collection.delete_many(query)
                print('Documents deleted:', result.deleted_count)
                return result.deleted_count
            except Exception as e:
                print('Delete failed:', e)
                return 0
        else:
            raise Exception("Query cannot be None")


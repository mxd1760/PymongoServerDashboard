from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self,user = 'aacuser',pwd = 'aacpass'):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31700
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (user,pwd,HOST,PORT),serverSelectionTimeoutMS=100)
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert_one(data)  # data should be dictionary   
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None:
            return self.database.animals.find(query)
        else:
            raise Exception("Nothing to find, because query parameter is empty")
         
# Second R method
    def read_one(self,query):
        if query is not None:
             return self.database.animals.find_one(query)
        else:
             raise Exception("Must provide query")
           
# method that finds the items that match the query and then applies the modification to them
    def update(self,query,modification):
    	if query is not None:
            if modification is not None:
                result = self.database.animals.update_many(query,modification)
                return result.modified_count
            else:
                raise Exception("a modification must be provided")
    	else:
    	    raise Exception("query to find the item to update must be provided")
    
# method that finds the items that match the query and then deletes them
    def delete(self,query):
    	if query is not None:
    	   result = self.database.animals.delete_many(query)
    	   return result.deleted_count
    	else:
    	   raise Exception("query to find the item to delete must be provided")
    	   
# filter methods
    def filter_water_rescue(self):
    	return self.read({\
    	"breed":{"$in":["Labrador Retriever Mix","Chesapeake Bay Retriever","Newfoundland"]}, \
    	"sex_upon_outcome":"Intact Female",\
    	"age_upon_outcome_in_weeks":{"$gte":26},\
    	"age_upon_outcome_in_weeks":{"$lte":156}})
    	
    def filter_mountain_or_wilderness_rescue(self):
    	return self.read({\
    	"breed":{"$in":["German Shepherd","Alaskan Malamute","Old English Sheepdog","Siberian Husky","Rottweiler"]},\
    	"sex_upon_outcome":"Intact Male",\
    	"age_upon_outcome_in_weeks":{"$gte":26},\
    	"age_upon_outcome_in_weeks":{"$lte":156}})
    
    def filter_disaster_or_individual_tracking(self):
    	return self.read({\
    	"breed":{"$in":["Doberman Pinscher","German Shepard","Golden Retriever","Bloodhound","Rottweiler"]},\
    	"sex_upon_outcome":"Intact Male",\
    	"age_upon_outcome_in_weeks":{"$gte":26},\
    	"age_upon_outcome_in_weeks":{"$lte":156}})
    
    def filter_none(self):
    	return self.read({})
    	

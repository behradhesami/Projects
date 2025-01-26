from pymongo import MongoClient
from datetime import datetime
from data import projects, users
from bson.objectid import ObjectId

"""
The program is a small example of a clockify.
"""

# Establish a connection to the MongoDB server running on localhost
client = MongoClient("mongodb://localhost:27017/")
# Select the database named 'Normalize'
db = client.Normalize

# Define collections for users, projects, and reports
user_collection = db.user
project_collection = db.project
report_collection = db.report

def store():
    """
    Store users and projects in the MongoDB collections.
    This function inserts multiple user and project records into the database.
    """
    user_collection.insert_many(users)  # Insert all users from the 'users' data
    project_collection.insert_many(projects)  # Insert all projects from the 'projects' data

def save_record():
    """
    Save a record of a user's project activity with a start time.
    This function retrieves a user and project by their identifiers,
    then creates a report entry with the current timestamp.
    """
    ali = user_collection.find_one({'username': 'ali'})  
    shop = project_collection.find_one({'name': 'onlineshop'}) 

    # Insert a new report record with user, project, and start time
    report = report_collection.insert_one({
        'user': ali,
        'project': shop,
        'start_time': datetime.now()
    })
    print(report.inserted_id) 

def end_time(object_id):
    """
    Update the end time of a report based on its ObjectId.
    This function finds a report by its ID and sets its end_time to the current timestamp.
    """
    query = {'_id': ObjectId(object_id)}  # Create a query to find the report by ID
    
    existing_record = report_collection.find_one(query)  
    if not existing_record:
        print(f"No record found with ID: {object_id}")  
        return

    update = {'$set': {'end_time': datetime.now()}}  # Prepare update to set end_time
    result = report_collection.update_one(query, update)  

    if result.modified_count > 0:
        print(f"Record with ID: {object_id} updated successfully.")  
    else:
        print(f"No records were updated for ID: {object_id}.")  

def show_report():
    """
    Display reports showing user activity duration on projects.
    This function calculates and prints the duration of each user's activity based on start and end times.
    """
    for reports in report_collection.find(): 
        duration = reports['end_time'] - reports['start_time']  
        print(f"{reports['user']['username']}\t {reports['project']['name']}\t{duration.seconds}")  

# end_time("678754c3f11fbbf3747fb5f4")

show_report()

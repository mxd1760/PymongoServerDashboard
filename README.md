
# Grazioso Salavare Animal Database Dashboard

## Functionality
This project intends to provide access to a mongodb database through the use of the pymongo python package and an interactive application developed with the dash framework. This kind of software allows for non-technical staff to access the data as well as view several useful visualizations of it.

## Tools Used
[MongoDB]( https://www.mongodb.com/ ) was selected as the database for this project because it formats data in a json like way which makes it easy to convert between the database and python dictionaries.
[Dash]( https://dash.plotly.com/ ) was used as the framework for the interface. It also uses several other packages such as [Pandas]( https://pandas.pydata.org/ ) for data modeling, and [plotly.express]( https://plotly.com/python/plotly-express/ ) for graphing.
[pymongo]( https://pymongo.readthedocs.io/en/stable/ ) was the last tool used. This allowed for the creating of python scripts that can easily interface with the mongo database.

## Steps for completion
First the data needed to be added to a mongodb instance and a user created through which the python scripts could access the data.
Second to be developed was the interface script that used pymongo to perform several of the basic CRUD tasks that the dashboard would end up needing.
The final step was to create the Dashboard script that leveraged the interface script to implement all of the features requested including a graph, a map, filtering options, and the ability to select specific entries from the dataset for more information.

## Challenges
I think it was challenging implementing many things that I knew how to do with the python packages that I wasn’t very familiar with. Even if I knew exactly what data I had and what I wanted to make, the unfamiliar frameworks made formatting the data properly more difficult as well as understanding what form it needed to be in. The error messages were also very unhelpful in comparison to tool’s I’m more accustomed to. Even after working through it all, I still prefer other tools for making websites and UI even if mongodb seems like a perfectly fine database option. While an expert at python might be able to develop this kind of thing faster than I can with my preferred tools, I find that that comes with giving up a lot of information and control which feels like it may often lead to outright dead ends instead of opportunities to solve new problems.

## Build Instructions
If you would like to test this software for yourself you will need to follow these steps to get it up and running

-	Install mongodb 
-	Use the aac_shelter_ooutcomes.csv file to populate a sample database
-	Create a user with access to this database to use in the python scripts
-	Download the AAC_ReadWrite.py and ProjectTwoDashboard.py files into a local folder
-	Before these files will work you will need to go into one or both of them to edit the username, password, and path to the database. If you didn’t name your database ‘AAC’ and the collection ‘animals’ you will need to change those too
-	In a terminal from the folder where your files are run the following 3 commands in order
```
pip install pipreqs
pipreqs .
pip install -r requirements.txt
```
These commands together should install all the necessary python dependencies for the files.
-	Once all dependencies are installed and both files have been configured to access the database you setup you should be ready to run `python ProjectTwoDashboard.py” to start a server that can be accessed from a browser with the link that should be provided.
     

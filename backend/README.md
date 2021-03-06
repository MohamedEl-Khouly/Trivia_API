# Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default,`http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require any form of authentication or API Keys.
### Error Handling

Errors are returned in JSON objects in the following format:
```
{ 
  "success": false,
  "error":404,
  "message": "Resource Not Found"
}

```
When a request fails the API sends one of the following errors:
- 400: bad request
- 404: Resource Not Found
- 422: Request cannot be procesed
### Endpoints

__GET__ `/categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns an object with the format of the following example 
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

__GET__ `\questions?page=<page_number>`

- Fetches a paginated list of questions of all available categories
- Request parameters (optional): page:int
- Returns an object with the format of the following example
```
{
	"categories": {
		"1": "Science", 
		"2": "Art", 
		"3": "Geography", 
		"4": "History", 
		"5": "Entertainment", 
		"6": "Sports"
  	}, 
  	"current_category": null,
	"questions": [
		{
			"answer": "Apollo 13",
			"category": 5,
			"difficulty": 4,
			"id": 2,
			"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
		},
		{
			"answer": "Tom Cruise",
			"category": 5,
			"difficulty": 4,
			"id": 4,
			"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		},
		{
			"answer": "Brazil",
			"category": 6,
			"difficulty": 3,
			"id": 10,
			"question": "Which is the only team to play in every soccer World Cup tournament?"
		},
		{
			"answer": "Uruguay",
			"category": 6,
			"difficulty": 4,
			"id": 11,
			"question": "Which country won the first ever soccer World Cup in 1930?"
		},
		{
			"answer": "George Washington Carver",
			"category": 4,
			"difficulty": 2,
			"id": 12,
			"question": "Who invented Peanut Butter?"
		},
		{
			"answer": "Lake Victoria",
			"category": 3,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		},
		{
			"answer": "The Palace of Versailles",
			"category": 3,
			"difficulty": 3,
			"id": 14,
			"question": "In which royal palace would you find the Hall of Mirrors?"
		},
		{
			"answer": "Agra",
			"category": 3,
			"difficulty": 2,
			"id": 15,
			"question": "The Taj Mahal is located in which Indian city?"
		}
	],
	"success": true,
	"total_questions": 19
}
```

__DELETE__ `/questions/<int:question_id>`

- Deletes a question from the table of questions storred in the APP database
- Request arguments: question_id:int
- Returns an object with the format of the following example
```
{
	"deleted": "2", 
	"success": true
}
```

__POST__ `/questions`

- Adds a new question to the table of questions storred in the  APP Database
- Requires a body of the following format 
```
{
	question:string,
	answer:string,
	difficulty:int,
	category:int
}
```
- Returns an object with the format of the following example
```
{
	"created": 29, 
	"success": true
}
```

__POST__ `/questions/search`

- Returns a list of questions containg the search term as a part of the question text
- search term is not case sensitive
- Requires a body of the following format
```
{
	'searchTerm': 'what'
}
```
- Returns an object with the format of the following example
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Lisbon", 
      "category": 2, 
      "difficulty": 1, 
      "id": 29, 
      "question": "What is the capital of Portugal?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

__GET__ `/categories/<int:category_id>/questions`

- Returns a list of the questions filtered by category.
- Arguments: category_id : int
- Returns an object with the format of the following example
```
{
	"current_category": 4,
	"questions": [
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		},
		{
			"answer": "George Washington Carver",
			"category": 4,
			"difficulty": 2,
			"id": 12,
			"question": "Who invented Peanut Butter?"
		},
		{
			"answer": "Scarab",
			"category": 4,
			"difficulty": 4,
			"id": 23,
			"question": "Which dung beetle was worshipped by the ancient Egyptians?"
		}
	],
	"success": true,
	"total_questions": 3
}
```
__POST__ `/quizzes`

- fetches a random question from the Database according to a specified category and excleding questions previously retrived

- Requires a body of the following format
```
{
	previous_questions: array of int, 
	quiz_category:{
		id:int,
		type:string
	}
}
```
- Returns an object with the format of the following example
```
{
	'success':true,
	'question':{

		"answer": "Scarab",
		"category": 4,
		"difficulty": 4,
		"id": 23,
		"question": "Which dung beetle was worshipped by the ancient Egyptians?"
	}
}
```

## Testing

The file test_flasker.py includes test scenarios for each endpoint

To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
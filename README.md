# API for sport contests

Allows users to create models of sport competitions and their participants as well as implement some interactions between these objects according to the requirements below


## Technical requirements

+ Create a user (check the email for validity), which can participate at contests in only one sport
+ Output the data of a requested user
+ Create a contest (sports: table tennis, boxing, ...). Initialize the "STARTED" status
+ Output the data of a requested contest
+ Finish a contest. Assign the winner, initialize the "FINISHED" status
+ Output the history of a user's contests
+ Generate the users list sorted by the amount of each user's contests
+ Generate the graph of users sorted by the amount of each user's contests

## Queries and responses

- Creating a user `POST /users/create`

Request example:
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "sport": "string"
}
```

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "contests": [
  	"number",
    ...
  ]
}
```

- Output the data of a requested user `GET /users/<user_id>`

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "contests": [
  	"number",
    ...
  ]
}
```

- Create a contest `POST /contests/create`

Request example:
```json
{
  "name": "string",
  "sport": "string",
  "participants": [
  	"number",
    "number"
  ]
}
```

Response example:
```json
{
  "id": "number",
  "name": "string",
  "sport": "string",
  "status": "STARTED",
  "participants": [
  	"number",
    "number"
  ],
  "winner": null
}
```

- Output the data of a requested contest `GET /contests/<contest_id>`

Response example:
```json
{
  "id": "string",
  "name": "string",
  "sport": "string",
  "status": "string",
  "participants": [
  	"number",
    "number"
  ],
  "winner": "number"
}
```

- Finish a contest `POST /contests/<contest_id>/finish`

Request example:
```json
{
  "winner": "number"
}

Response example:
```json
{
  "id": "string",
  "name": "string",
  "sport": "string",
  "status": "FINISHED",
  "participants": [
  	"number",
    "number"
  ],
  "winner": "number"
}
```

- Output the history of a user's contests `GET /users/<user_id>/contests`

Response example:
```json
{
  "contests": [
  	{
    	"id": "string",
        "name": "string",
        "sport": "string",
        "status": "FINISHED",
        "participants": [
          "number",
          "number"
  		],
  		"winner": "number"
    }
    {
    	...
    }
  ],
}
```

- Generate the users list sorted by the amount of each user's contests `GET /users/leaderboard`

Values `asc`and `desc` stand for `ascending` and `descending` respectively

Request example:
```json
{
"type": "list",
"sort": "asc/desc"
}
```

Response example:
```json
{
  "users": [
    {
      "id": "number",
  "first_name": "string",
      "last_name": "string",
      "email": "string",
      "contests": [
        "number",
        ...
      ]
 },
 {
    	...
    }
  ],
}
```

- Generate the graph of users list sorted by the amount of each user's contests `GET /users/leaderboard`

Request example:
```json
{
  "type": "graph",
}
```

Response example:
```html
<img src="path_to_graph">
```
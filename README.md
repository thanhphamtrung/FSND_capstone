# Casting agency doc

Casting agency api is a tool that provides endpoints to support you create an application to manage casting.

I developed this project to make use of the knowledge I acquired in Udacity nanogree and hence gain confidence in these skills.

## Login
<a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a>

The access token will be displayed on the URL bar after login.

## THIRD-PARTY AUTHENTICATION
### RABC
- There are 3 roles 'Casting Assistant', 'Casting Director' and 'Executive Producer'.
- To get access token for 'Casting Assistant', login with account:
    - username: casting_assistant@gmail.com
    - password: Abcd1234
- To get access token for 'Casting Director', login with account:
    - username: casting_director@gmail.com
    - password: Abcd1234
- To get access token for 'Executive Producer', login with account:
    - username: executive_producer@gmail.com
    - password: Abcd1234

### auth.py
Auth0 is set up and running. The following configurations are in a setup.sh file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'Executive Producer' roles.

## DATA MODELING:
### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are three tables created: Movie, Acotr and Casting
- The Movie table is used by the role 'Executive Producer' to add, update and create movies. 'Casting Director' and 'Casting Assistant' can retrieve movie list.
- The Actor table is used by the role 'Executive Producer' and 'Casting Director' to add, update and create actors. 'Casting Assistant' can retrieve actor list.
- The Casting table is used by the role 'Executive Producer', 'Casting Director' and 'Casting Assistant' to add, update and create castings and retrive all casting data
- The Casting table has 2 foreign keys 'actor_id' and 'movie_id' for both Actor and Movie table.
Each table has an insert, update, delete, and format helper functions.

## Run and Test local
1. Run venv

    ```
    python3.9 -m venv venv
    ```

2. Setup environment

    ```
    source venv/bin/activate
    source setup.sh
    ```

3. Install dependencies
    
    ```
    pip3 install -r requirements.txt
    ```

4. Create a new database and import new data for testing
    
    ```
    dropdb casting-agency # (optional) Drop if it exists 
    createdb casting-agency
    psql -U postgres -d casting-agency < database.sql
    ```

5. Run the app

    ```
    flask run -p 3000
    ```


6. Login in local

    <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=http://localhost:3000/">Login locally</a>
    The access token will be displayed on the URL bar after login.

7. Run unittest
   ```
   python3 test_flask.py
   ```

8. Run test

    In Postman, import file **casting-agency.postman_collection.json** to run the test.

    If the tokens expire, please login locally again to get the token for respectively roles.

## Use API
### Resource endpoint library

#### GET '/movies'

- Return a list of movies in database
- Sample curl:

    ```
      curl -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/movies
    ```

- Sample response

    ``` json
    {
        "movies": [
            {
                "director": "Seymour Huikerby",
                "facebook_link": "http://google.com",
                "genres": "Adventure,Sci-Fi",
                "id": 1,
                "image_link": "http://google.com",
                "name": "Dune",
                "phone": "123412343",
                "producer": "Dach-Streich",
                "seeking_actor": true,
                "seeking_description": "Finding actors for Dune movie",
                "website": "http://dune.com"
            },
            {
                "director": "Juliane Pexton",
                "facebook_link": "166.11.226.15",
                "genres": "Drama",
                "id": 2,
                "image_link": "27.215.169.113",
                "name": "A Magnificent Haunting",
                "phone": "241 789 3774",
                "producer": "Dooley Group",
                "seeking_actor": true,
                "seeking_description": "˙ɐnbᴉlɐ ɐuƃɐɯ ǝɹolop ʇǝ ǝɹoqɐl ʇn ʇunpᴉpᴉɔuᴉ ɹodɯǝʇ poɯsnᴉǝ op pǝs 'ʇᴉlǝ ƃuᴉɔsᴉdᴉpɐ ɹnʇǝʇɔǝsuoɔ 'ʇǝɯɐ ʇᴉs ɹolop ɯnsdᴉ ɯǝɹo˥",
                "website": "190.29.216.110"
            }
        ],
        "success": true,
        "total_movies": 2
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### GET '/movies?searchTerm=search_term'
- Search movies in database by searchTerm
- Sample curl:

    ```
    curl -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/movies?searchTerm=Dune
    ```

- Sample response

    ``` json
    {
        "movies": [
            {
                "director": "Seymour Huikerby",
                "facebook_link": "http://google.com",
                "genres": "Adventure,Sci-Fi",
                "id": 1,
                "image_link": "http://google.com",
                "name": "Dune",
                "phone": "123412343",
                "producer": "Dach-Streich",
                "seeking_actor": true,
                "seeking_description": "Finding actors for Dune movie",
                "website": "http://dune.com"
            }
        ],
        "success": true,
        "total_movies": 1
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### GET '/movies/{movie_id}'
- Get specific infor of a movie id
- Sample curl:

    ```
    curl -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/movies/1
    ```

- Sample response

    ``` json
    {
        "movie": {
            "director": "Seymour Huikerby",
            "facebook_link": "http://google.com",
            "genres": "Adventure,Sci-Fi",
            "id": 1,
            "image_link": "http://google.com",
            "name": "Dune",
            "phone": "123412343",
            "producer": "Dach-Streich",
            "seeking_actor": true,
            "seeking_description": "Finding actors for Dune movie",
            "website": "http://dune.com"
        },
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### PATCH '/movies/{movie_id}'
- Update a movie id infomation
- Sample curl:

    ```
      curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/movies/1 \
      -F director:Seymour Huikerby \
      -F facebook_link:http://google.com \
      -F genres:Adventure \
      -F genres:Sci-Fi \
      -F image_link:http://google.com \
      -F name:Dune \
      -F phone:123412343 \
      -F producer:Dach-Streich \
      -F seeking_actor:true \
      -F seeking_description:Finding actors for Dune movie \
      -F website:http://dune.com
    ```

- Sample response

    ``` json
    {
        "movie": {
            "director": "Seymour Huikerby",
            "facebook_link": "http://google.com",
            "genres": "Adventure,Sci-Fi",
            "id": 1,
            "image_link": "http://google.com",
            "name": "Dune",
            "phone": "123412343",
            "producer": "Dach-Streich",
            "seeking_actor": true,
            "seeking_description": "Finding actors for Dune movie",
            "website": "http://dune.com"
        },
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with 'Executive Producer' role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter that credential into Auth0.

#### POST '/movies'
- Create a new movie
- Sample curl:
  
    ```
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/movies \
      -F director:Seymour Huikerby \
      -F facebook_link:http://google.com \
      -F genres:Adventure \
      -F genres:Sci-Fi \
      -F image_link:http://google.com \
      -F name:Dune \
      -F phone:123412343 \
      -F producer:Dach-Streich \
      -F seeking_actor:true \
      -F seeking_description:Finding actors for Dune movie \
      -F website:http://dune.com
    ```

- Sample response

    ``` json
    {
        "movie": {
            "director": "Seymour Huikerby",
            "facebook_link": "http://google.com",
            "genres": "Adventure,Sci-Fi",
            "id": 17,
            "image_link": "http://google.com",
            "name": "Dune",
            "phone": "123412343",
            "producer": "Dach-Streich",
            "seeking_actor": true,
            "seeking_description": "Finding actors for Dune movie",
            "website": "http://dune.com"
        },
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with 'Executive Producer' role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter that credential into Auth0.

#### DELETE '/movies/{movie_id}'
- Delete a movie by id
- Sample curl:

    ```
    curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/movies/10
    ```

- Sample response

    ``` json
    {
        "id": "10",
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with 'Executive Producer' role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter that credential into Auth0.

#### GET '/actors'
- Return a list of actors in database
- Sample curl:

    ```
    curl -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/actors
    ```
  
- Sample response:

    ``` json
    {
        "actors": [
            {
                "age": 43,
                "city": "Norman",
                "genres": "Comedy,Drama",
                "id": 1,
                "image_link": "http://google.com",
                "name": "Arabela Lebbern",
                "phone": "4056375359",
                "seeking_description": "I want a movie",
                "seeking_movie": true,
                "sex": "Male",
                "state": "AL",
                "website": "http://google.com"
            },
            {
                "age": 55,
                "city": "Spartanburg",
                "genres": "Drama",
                "id": 2,
                "image_link": "175.158.204.166",
                "name": "Amandi Grewcock",
                "phone": "8641139421",
                "seeking_description": "",
                "seeking_movie": true,
                "sex": "Female",
                "state": "South Carolina",
                "website": "65.11.237.63"
            }
        ],
        "success": true,
        "total_actors": 2
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### GET '/actors?searchTerm=search_term'
- Return a list of movies that match the search term
- Sample curl:

    ```
    curl -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/actors?searchTerm=Jeff
    ```

- Sample response:

    ``` json
    {
        "actors": [
            {
                "age": 27,
                "city": "New Castle",
                "genres": "Comedy|Crime|Romance",
                "id": 3,
                "image_link": "84.76.160.39",
                "name": "Jeff Petrushka",
                "phone": "7247585798",
                "seeking_description": "!@#$%^&*()",
                "seeking_movie": true,
                "sex": "Male",
                "state": "Pennsylvania",
                "website": "231.90.43.230"
            }
        ],
        "success": true,
        "total_actors": 1
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### GET '/actors/{actor_id}'
- Return actor info of an actor
- Sample curl:

    ```
    curl -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/actors/1
    ```

- Sample response:

    ``` json
    {
        "actor": {
            "age": 43,
            "city": "Norman",
            "genres": "Comedy,Drama",
            "id": 1,
            "image_link": "http://google.com",
            "name": "Arabela Lebbern",
            "phone": "4056375359",
            "seeking_description": "I want a movie",
            "seeking_movie": true,
            "sex": "Male",
            "state": "AL",
            "website": "http://google.com"
        },
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### PATCH '/actors/{actor_id}'
- Update actor info by id
- Sample curl:

    ```
    curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/actors/1 \
    -F age:43 \
    -F city:Norman \
    -F genres:Comedy \
    -F genres:Drama \
    -F image_link:http://google.com \
    -F name:Arabela Lebbern \
    -F phone:4056375359 \
    -F seeking_description:I want a movie \
    -F seeking_movie:true \
    -F sex:Male \
    -F state:AL \
    -F website:http://google.com
    ```

- Sample response:

    ``` json
    {
        "actor": {
            "age": "43",
            "city": "Norman",
            "genres": "Comedy,Drama",
            "id": 1,
            "image_link": "http://google.com",
            "name": "Arabela Lebbern",
            "phone": "4056375359",
            "seeking_description": "I want a movie",
            "seeking_movie": true,
            "sex": "Male",
            "state": "AL",
            "website": "http://google.com"
        },
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with 'Executive Producer' or 'Casting Director' role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter that credential into Auth0.

#### POST '/actors'
- Create a new actor
- Sample curl

    ```
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/actors \
    -F age:43 \
    -F city:Norman \
    -F genres:Comedy \
    -F genres:Drama \
    -F image_link:http://google.com \
    -F name:Arabela Lebbern \
    -F phone:4056375359 \
    -F seeking_description:I want a movie \
    -F seeking_movie:true \
    -F sex:Male \
    -F state:AL \
    -F website:http://google.com
    ```

- Sample response

    ``` json
    {
        "actor": {
            "age": null,
            "city": "Norman",
            "genres": "Comedy,Drama,Romance,War",
            "id": 11,
            "image_link": "http://google.com",
            "name": "Arabela Lebbern",
            "phone": "4056375359",
            "seeking_description": "I want a movie",
            "seeking_movie": true,
            "sex": null,
            "state": "AL",
            "website": "http://google.com"
        },
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with 'Executive Producer' or 'Casting Director' role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter that credential into Auth0.

#### DELETE '/actors/{actor_id}'
- Delete an actor by id
- Sample curl

    ```
    curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/actors/11
    ```

- Sample response

    ``` json
    {
        "id": "11",
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with 'Executive Producer' or 'Casting Director' role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter that credential into Auth0.

#### GET '/castings'
- Return a list of castings in database
- Sample curl

    ```
    curl -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/castings
    ```

- Sample response

    ``` json
    {
        "castings": [
            {
                "actor_id": 1,
                "id": 1,
                "movie_id": 1,
                "place": "23rd Lincon street",
                "start_time": "2014-12-11 23:30:34"
            },
            {
                "actor_id": 1,
                "id": 2,
                "movie_id": 1,
                "place": "342street",
                "start_time": "2014-12-11 23:30:34"
            }
        ],
        "success": true,
        "total_castings": 2
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### POST '/castings'
- Create a new casting
- Sample curl

    ```
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/castings \
    - F actor_id:1 \
    - F movie_id:1 \
    - F start_time:2014-12-11 23:30:34 \
    - F place:342street
    ```

- Sample response

    ``` json
    {
        "casting": {
            "actor_id": "1",
            "id": 3,
            "movie_id": "1",
            "place": "342street",
            "start_time": "2014-12-11 23:30:34"
        },
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.

#### DELETE '/castings/{casting_id}'
- Delete a casting by id
- Sample curl

    ```
    curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:3000/castings/1
    ```

- Sample response

    ``` json
    {
        "id": "3",
        "success": true
    }
    ```

- To get the tokens for this endpoints, we have to login with any role permission that is listed in RABC section.
  Click on <a href="https://fsnd-stu.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=2NqLLf0o0DJrhgYUOhbSWHttGWPaM7gI&redirect_uri=https://casting-agency-api.onrender.com/">Login</a> and enter one of those credentials into Auth0.


### Error handling
All error return a json object with these keys: success, error and message

#### Error 400
  ``` json
    {
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }
  ```

#### Error 404
  ``` json
    {
      "success": False,
      "error": 404,
      "message": "Not Found"
    }
  ```

#### Error 405
  ``` json
    {
      "success": False,
      "error": 405,
      "message": "Method Not Allowed"
    }
  ```

#### Error 422
  ``` json
    {
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }
  ```

#### Error 500
  ``` json
    {
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }
  ```
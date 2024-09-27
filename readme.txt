Here are the Step for projects Working

Step 1: POST http://127.0.0.1:8000/api/register/

{
  "username":"Rohit",
  "password":123
}
{
  "username":"Ganesh",
  "password":123
}


Step 2: POST http://127.0.0.1:8000/api/token/

input: {
  "username":"Rohit",
  "password":123
}

Here Token is generate  then copy that token 
put it in Header AUthorization: Bearer Token...

Step 3:POST http://127.0.0.1:8000/api/clients/
input: 
{
  "client_name":"Nimap";
}

Step 4:  GET http://127.0.0.1:8000/api/clients/            //it will get all client list

Step 5:  GET http://127.0.0.1:8000/api/clients/{:id}/      //it will get client according to id and also shows project assigned to that client

step 6: POST http://127.0.0.1:8000/api/clients/{:id}/projects/
Input:
{
    "project_name": "Project A",
    "users": [
        {
            "id": 1,
            "username": "Rohit"
        }
    ]
}
step 7: GET http://127.0.0.1:8000/api/projects/       Here it show All project list along with details


----------------------------
step 8: PUT http://127.0.0.1:8000/api/clients/:id/     PUT Method //For updation
{
  "client_name":"Update name here";                        // it will update the name of the client
}
step 8: DELETE http://127.0.0.1:8000/api/clients/:id/     //Deletion Request
                                                         // it will Delete the client



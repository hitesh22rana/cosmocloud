# FastAPI Organization Management API

This is a FastAPI-based API for managing organizations and their members. It allows users to create organizations, add members to them, update members' access levels, and delete organizations.

## Requirements

- Python 3.9 or higher
- MongoDB
- Docker and docker-compose (optional)

## Installation

### **Using Docker**

1. Clone the repository.

```bash
git clone https://github.com/hitesh22rana/cosmocloud.git
cd cosmocloud
```

2. Now run the following command to start the application.

```bash
docker-compose -f docker-compose.yml up --build -d
```

3. The API will be available at http://localhost:8000.

### **Using Python**

1. Clone the repository.

```bash
git clone https://github.com/hitesh22rana/cosmocloud.git
cd cosmocloud
```

2. Create a virtual environment.

```bash
virtualenv venv
```

3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file based and add the following environment variables.

```bash
DATABASE_HOSTNAME=mongodb://localhost
DATABASE_PORT=27017
DATABASE_NAME=cosmocloud
```

5. Start the server by running the following command.

```bash
`uvicorn app.main:app --reload`
```

6. The API will be available at http://localhost:8000.

## Endpoints

### **Users**
- `GET /users/`: Retrieves a list of all users, optionally filtering by name, limit, and offset.
- `GET /users/{user_id_or_email}`: Retrieves a user by its ID or email (As both are unique).
- `POST /users/`: Creates a new user.

### **Orgnizations**
- `GET /organizations`: Retrieves a list of all organizations, optionally filtering by name, limit, and offset.
- `GET /organizations/{id_or_name}`: Retrieves an organization by its ID or name (As both are unique).
- `POST /organizations/`: Creates a new organization.
- `POST /organizations/{organization_id}/members/{author_id}/`: Adds a member to an organization.
- `PATCH /organizations/{organization_id}/members/{author_id}`: Updates a member's access level in an organization.
- `DELETE /organizations/{organization_id}/members/{author_id}`: Removes a member from an organization.

## Errors

This API uses HTTP status codes to indicate the success or failure of requests. When an error occurs, the response body will include a JSON object with a `detail` key that describes the error in more detail.

## Technologies Used
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Pymongo](https://pymongo.readthedocs.io/en/stable/)
- [Motor Driver](https://motor.readthedocs.io/en/stable/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
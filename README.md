# Saikiran Assignment


## Project Overview
This project processes and provides APIs for trip data analysis, including RESTful and GraphQL endpoints. 

---

## Prerequisites
- **Docker** and **Docker Compose** must be installed on your system.
- Ensure you have the `test.csv` file located at `/Users/saikiran/Downloads/nyc/test.csv`.

---

## Getting Started

### 1. Setup the Data Directory
Create the `data` directory and copy the dataset into it:
```bash
mkdir -p data
cp "/Users/saikiran/Downloads/nyc/test.csv" data/
2. Build and Start the Application
Ensure all services are stopped, then rebuild and start the application without using cache:

bash
Copy code
docker-compose down
docker-compose build --no-cache
docker-compose up

3. Access the API Documentation
Once the services are running, navigate to the following URL to access the API documentation:

API Documentation
http://0.0.0.0:8000/docs

API Endpoints
RESTful Endpoints
Get Trips

Method: GET
URL: /api/v1/trips/
Description: Retrieve a list of all trips.
Get Trip Stats

Method: GET
URL: /api/v1/trips/stats
Description: Retrieve statistical data for trips.
Process Trip Data

Method: GET
URL: /api/v1/trips/process
Description: Process and prepare trip data for analysis.
GraphQL Endpoints
GraphQL Query

Method: GET
URL: /graphql
Description: Query data using GraphQL.
GraphQL Mutation

Method: POST
URL: /graphql
Description: Submit data modifications or complex queries using GraphQL.


Ensure the Docker container is up and running to interact with the APIs.
All endpoints are accessible at http://0.0.0.0:8000.
Update the dataset (test.csv) as required in the data directory for different analysis scenarios.
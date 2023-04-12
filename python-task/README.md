# RAI_homework_Python Task

To run the project, you need to have docker and docker-compose installed.

In your terminal/console, navigate to *python-task* project folder and run command:
```
docker-compose up
```
Once you see messages bellow you can open this [url](http://0.0.0.0:5002/) in your browser:
```
api2           | INFO:     | 2023-04-12 16:26:09 | Server started.
api2           | INFO:     Application startup complete.
api1           | INFO:     | 2023-04-12 16:26:10 | Server started.
api1           | INFO:     Application startup complete.
```


#### Project components:
1. PostgreSQL DB(for storing list of countries and priority codes)
2. First API service (Country object) - FastAPI service
3. Second API service (Priority object) - FastAPI service
4. GUI service - Ploty/Dash service


##### Full workflow test:
https://github.com/milanchanstveni/revenue.ai/blob/main/python-task/python-task.mp4?width=200&height=200



#### Test:
To run tests, navigate to *python-task* project folder and run commands:
```
docker-compose up -d
pytest tests
```

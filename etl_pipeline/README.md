# Python Interview Prep Challenges

## Building the Docker Container

To build the container:

- Spin up a Docker Daemon (Docker Desktop)

- `cd ./pyspark_training`
- `docker-compose build`

## Running the Script

To run the walkthrough:

- `cd ./pyspark_training`
- `make submit app=walkthrough/pyspark_practice.py`

## Spark Questions

1. What is the difference between a master and a worker node?

2. What is the difference between:
    - RDD
    - Dataframe
    - Dataset

3. How do joins work between distributed clusters?

4. Explain the concept of a broadcast join, and when a broadcast join might be useful.

5. How would you navigate addressing situations like data skew?


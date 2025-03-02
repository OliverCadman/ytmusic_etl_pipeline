# YTMusic ETL Pipeline

An ETL pipeline which will be run on a monthly schedule, and fed to a dashboard to provide insights of my listening trends on Youtube Music; I guess you could call it my very own 'Youtube Unwrapped' dashboard.

## Technologies Used

- Extraction and staging
    - AWS S3 (using the boto3 client)

- Transformations
    - PySpark
    - Docker

- Data Warehousing
    - AWS S3

- Scheduling
    - Apache Airflow

- Dashboarding
    - TBC (will possibly build a dashboard myself using ReactJS)

I will be tinkering away on this project when I find the time. Currently
the functionality is in place to load raw source data into an S3 bucket
for staging. I will update this README as I progress in the project.
build:
		docker-compose build

build-nc:
		docker-compose build --no-cache

build-progress:
		docker-compose build --no-cache --progress=plain

down:
		docker-compose down --volumes

run:
		make down && docker-compose up

run-scaled:
		make down && docker-compose up --scale spark-worker=3

run-d:
		make down && docker-compose up -d

stop:
		docker-compose stop

submit:
		docker exec da-spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./$(app)

submit-s3:
		docker exec da-spark-master spark-submit --master spark://spark-master:7077 --jars /opt/spark/jars/aws-java-sdk-bundle-1.12.782.jar,/opt/spark/jars/hadoop-aws-3.4.1.jar --deploy-mode client ./$(app)
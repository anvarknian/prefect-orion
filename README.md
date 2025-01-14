# Prefect 2.0 docker compose deployment

Scripts to deploy Prefect 2.0 locally configured with Postgres, a docker agent, and Minio for flow storage


### Requirements
    * docker
    * docker-compose
    * make


### Steps

Clone this repo
Add folowing entry to your /etc/hosts:

```bash
127.0.0.1 prefect-server
```

Build docker image used by prefect server, agent and flow runner

```bash
make docker
```

Start the stack:

```bash
./prefect.sh start
```

The prefect.sh script initializes postgres and starts all services. Data (postgres, minio) is stored in a folder named `volumes`
Give the start command a few seconds, specially the first time since postgres and prefect need to be initialized
Open http://prefect-server:4200 in your browser and verify Prefect UI is up and running


Deploy client app to S3(minio):
```bash 
docker-compose up -d app
```

**OR**

Deploy client app to Docker registry:
```bash 
make register-test-flow
```

A flow named `my-docker-flow` and a `my-docker-flow/docker-example` deployment should have been created

Create a flow run from the `Deployments` screen by selecting the deployment and clicking on `Run`


To stop the services run `./prefect.sh stop`
To reset your environment, run `./prefect.sh reset && ./prefect.sh start`. A fresh deployment will start up.


### Notes
If running in linux, you may need to run as root depending on docker permissions
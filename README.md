# App0Platform: A Stateless-microservices-platform
This is a prototype/proof of concept of a Stateless Platform of Microservices Apps with a Python backend apps (hopeit.engine) and Vue 3 ui apps.

This repo shows and end-to-end example of a modern and scalable production-ready ecosystem of apps:
* Single SingOn
* Stateless microservices in Docker containers
* Python backend with an API based on hopeit.engine, an open-source library that enables to quickly develop microservices in Python. [Hopeit.engine](https://github.com/hopeit-git/hopeit.engine) is built on top of aiohttp to provide API endpoints and async processing, and also provides distributed processing of streaming events using Redis Streams. Streaming data, authorization, logging, metrics and tracking/tracing are added to your microservice out of the box.
* UI Apps with - [Vue 3](https://vuejs.org/) with Composition API, 
[vitejs](https://github.com/vitejs/vite) for build & development tool and [Typescript](https://github.com/microsoft/typescript) support out of the box.

This sample pretend to tackle some common needs when you start a new project like user manager, mail sending, logging, ci pipeline, containerize in dockers and orchestration in kubernetes.

Platform is compound of:
- `app0-admin` Platform manager backend (Apps, Users & Roles)
- `app0-admin-ui` Platform manager UI
- `app0-app1` Simple app1 backend to manage a simple workflow of claims
- `app0-app1-ui` Simple app1 UI to manage a simple workflow of claims
- `app0-app2` Simple app2 backend to manage company clients & services
- `app0-app2-ui` Simple app2 UI to manage company clients & services

## Prerequisites

1. A good code editor. I recommend [VSCode](https://code.visualstudio.com/). Settings are preconfigured if you start code on app or ui folder.
1. An python 3.8+ env. I recommend [Anaconda](https://docs.anaconda.com/anaconda/install/), but feel free to use `venv` or another.
1. [Nodejs LTS](https://nodejs.org/en/) _(14.x with npm >7)_ installed
1. [Typescript](https://github.com/microsoft/typescript) _(4.x)_ installed
1. [docker](https://docs.docker.com/engine/install/) & [docker-compose](https://docs.docker.com/compose/install/) installed

### Dockers

This project make use of certains dockers that are autoinstalled by docker:
* `Minio` as AWS S3 compatible object storage
* `MongoDb` as NoSQL database
* `Redis` to deliver data streams
* `nginx` as the api-gateway

## Getting started

This platform try to model a simple real world app for a company that provide services to clients and manage claims about services subscripted.

### App0-admin

- Provide Login and related funcionality
- Provide Registration for new users
- Manage Apps
- Manage Roles
- Manage Plans
- Manage Registrations
- Provide mailing capabilities
- Provide object storage capabilities

### App0-app1

- Some app...

### App0-app2

- Some other app...

## Run the platform

### First time use

- Go to `http://localhost:8021/api/docs/` & run `setup-db` endpoint with `FORCE` parameter. It will create all needed mongo collections, some base roles, and a superadmin account to login to platform: superuser / 123456
- To test setup, go to Authentication an set username and password, and run `Auth: Login` endpoint. If everything was OK, you would receive something like this:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjYyODI0YzUxNmJlZTNhZTc0YjVjNzUxNCIsInVzZXIiOiJzdXBlcnVzZXIiLCJmdWxsbmFtZSI6IlN1cGVydXNlciBBZG1pbiIsImVtYWlsIjoic3VwZXJ1c2VyQGFwcDAubWUiLCJlbXBsb3llZV9pZCI6IiIsImltYWdlIjoiIiwicm9sZXMiOlsiQXBwMCBVc2VyIiwiQXBwMCBBZG1pbiJdLCJncm91cHMiOltdLCJhcHAiOiJwbGF0Zm9ybV9hdXRoLjF4MCIsImlhdCI6MTY1MjcwNjc1MCwiZXhwIjoxNzEyNzA2NzUwLCJyZW5ldyI6NTk5OTk5OTQ5ODV9.iry2rdO1c1_1DekusQR6yM_S7Bth_iyaMrgYQSTKmtJqY4SL-DMmv0-GP_6hdZpjoVv1qqjZ25-vp9czElCvL5kyPme2nxAyuv_doS9btzF3OgKr1Ejn63R-5PNq3Ti_qL_4lF9HbCZfnelDLtQi52_WshGwoST2pn53Zs9MhhWu_MXYa_thyQwm-ot2XYVaDBcxd_7h-hYV24aI5g_TcC9Rx1h2blNFf3Dl9b4aekRt68uSvEKaR-flHOnCNOzGuwwx_FtauUUELAD6HyC_v_8qq8IQMFhVAIevZWGeoWrXpcUVDTxH0pbXsyOCoCjoublzbIyj5-ATY3h_OIkojw",
  "token_type": "BEARER",
  "renew": 59999994985
}
```






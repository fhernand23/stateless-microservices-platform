# Stateless-microservices-platform
This is a prototype/proof of concept of a Stateless Platform of Microservices Apps with a Python backend apps (hopeit.engine) and Vue 3 ui apps.

This repo shows and end-to-end example of a modern and scalable production-ready ecosystem of apps:
* Single SingOn
* Stateless microservices in Docker containers
* Python backend with an API based on hopeit.engine, an open-source library that enables to quickly develop microservices in Python. [Hopeit.engine](https://github.com/hopeit-git/hopeit.engine) is built on top of aiohttp to provide API endpoints and async processing, and also provides distributed processing of streaming events using Redis Streams. Streaming data, authorization, logging, metrics and tracking/tracing are added to your microservice out of the box.
* UI Apps with - [Vue 3](https://vuejs.org/) with Composition API, 
[vitejs](https://github.com/vitejs/vite) for build & development tool and [Typescript](https://github.com/microsoft/typescript) support out of the box.

This sample pretend to tackle some common needs when you start a new project like user manager, mail sending, logging, ci pipeline, containerize in dockers and orchestration in kubernetes.

Platform is compound of:
- `app-admin` backend of platform manager (Apps, Users & Roles)
- `app-admin-ui` ui of platform manager
- `app-claim` backend of a simple app to manage a workflow of claims
- `app-claim-ui` ui of a simple app to manage a workflow of claims
- `app-client` backend of a simple app to manage company clients
- `app-client-ui` ui of a simple app to manage company clients

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





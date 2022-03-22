# app0-admin

Admin App for platform `app0`
Application Manager for Single SignOn & show available apps.

## Development

### Create a conda environment

```bash
conda create -n app0-admin python=3.9
conda activate app0-admin
```
Install dependencies & modules
```bash
make dev-deps
make install
```

### Platform 1rst time setup

Run endpoint `setup-db` with `FORCE` keyword as parameter from API.

This should delete (if exist) and create all necessary collections and create some Test data:
- Superadmin: `superuser / 123`
- Company: `Company1`
- User1: `james@company / 123` (User Manager)
- User2: `mary@company / 123` (User Public Adjuster)
- User3: `jennifer@company / 123` (User Assistant)
- Provider1: `robert@mail` (Estimator)
- Provider2: `john@mail` (Appraiser)
- Provider3: `michael@mail` (Umpire)
- Provider4: `william@mail` (Attorney)

IMPORTANT: Remind disable setup-db endpoint after running it

### VS Code Debugging & Code style

- `/.vscode/launch.json`
- `/.vscode/settings.json`

## CI/CD

### Package registry: new version

To deliver a new version of app0-admin:

- increase version in `version.py` and merge-request on `main`
- Gitlab -> Merge request -> New Merge Request
- Source branch => main; Target branch => pip-publish
- `app0-attendant` => update dependencies in `requirements.txt`

## Docker

### Convinient set of `make` helpers:


Build API Container
```
make build-docker-api
```

Build Frontend Container:
```
make build-docker-ui
```

Build hopeit.engine Apps Visulizer Container:
```
make build-docker-apps-visualizer
```

Also, build API & UI Container in `app0-attendant`
```
cd ../app0-attendant
make build-docker-api
make build-docker-ui
```


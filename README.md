# How to use

1. Make sure your local environment is correctly configured

setup your GCP project ID

```
gcloud config set project [YOUR-PROJECT-ID]
```

Authenticate for the gcloud commands

```
gcloud auth login
```


setup your dev authentication for appplication default credentials. Although you could develop using your credentials, it is recommended to develop by impersonating a service account, as this is the identity that will be used at deployment time.

```
gcloud auth application-default login --impersonate-service-account [YOUR-SERVICE-ACCOUNT]
```


1. Install the dependencies

```
poetry install
```

2. Modify the variables in .env to fit your configuration

# Dev locally

```
make dev
```

If you try to stop the app, but it doesn't stop with Control-C, use the follwing command to kill it

```
kill $(ps -aux | grep mesop | awk '{print $2}')
```

# Deploy

Export your poetry dependencies to requirements.txt

```
poetry export -f requirements.txt --output requirements.txt
```

To avoid potential memory issues, it is recommended to allocate enough CPU and memory

```
gcloud run deploy simple-chat --project=[YOUR-PROJECT]  --service-account=[YOUR-SERVICE-ACCOUNT] --max-instances=1 --region=europe-west4 --allow-unauthenticated --source=. --cpu=4 --memory=8Gi
```
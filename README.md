# custom-churchtools-calendar-service



### Build
Before you build the Docker container, enter your churhtools credentials in the /secret/churchtools_credentials.json file
```
docker build -t <tag> .
```

### Run the Service
```
docker run -p 80:80 <tag>
```

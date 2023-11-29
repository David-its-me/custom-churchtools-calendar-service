# custom-churchtools-calendar-service

This sercie


### Build
The service is made as a Docker container. Before you build the container, please enter your churchtools credentials in the [/secret/churchtools_credentials.json](/secret/churchtools_credentials.json) file.
In order to build an run the Docker container, Docker must be installed on your system already.
If everithing is setup open a terminal go into the root directory of this reposiory and build the project with the following command:
```
docker build -t <tag> .
```
Please invent your own <tag> name for the container.

### Run the Service
After build was successful you can run your container image with the follwing command:
```
docker run -p 80:80 <tag>
```
The -p opens a port between the operating system and the container, to be able to access the container.

Now you can open http://127.0.0.1/ or http://localhost/

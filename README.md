# custom-churchtools-calendar-service

This service polls calendar entries and event data from a churchtools server and generates annoucement slides that visualize upcomming events.

### Build a Container Image
The service is made as a Docker container. Before you build the container, please enter your churchtools credentials in the [/secret/churchtools_credentials.json](/secret/churchtools_credentials.json) file.
In order to build an run the Docker container, Docker must be installed on your system already.
If everithing is setup open a terminal go into the root directory of this reposiory and build the project with the following command:
```
docker build -t <tag> .
```
Please invent your own name for the container image in ```<tag>```.

### Run the Container Image
After build was successful you can run your container image with the follwing command:
```
docker run -p 80:80 <tag>
```
The ```-p```-p opens a port between the operating system and the container, to be able to access the container.

Now you can open http://127.0.0.1/ or http://localhost/

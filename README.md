# Custom Churchtools Calendar Service

This service polls upcomming calendar entries and event data from a churchtools server and generates annoucement slides that visualize the upcomming events.

The visualization is based on our Cooporate Identity of our church. See our webpage: https://www.luho.de/.

## Build the Container Image
The service is made as a Docker container. Before you build the container, please enter your churchtools credentials in the [/secret/churchtools_credentials.json](/secret/churchtools_credentials.json) file.

After that you can build an run the Docker container. Please be aware that Docker must already be installed on your operating system. Here you can find more infromation about docker: https://docs.docker.com/.

If everything is setup, open a terminal and go into the root directory of this reposiory. There you can build the project with the following command:
```
docker build -t <tag> .
```
Please invent your own name for the container image in the ```<tag>``` variable.

## Run the Container Image
After build was successful you can run your container image with the follwing command:
```
docker run -p 80:80 <tag>
```
The ```-p``` option opens a port between the operating system and the container, to be able to access the container on port 80.

Now you can open http://127.0.0.1/ or http://localhost/ and see if everything is working!

## Custom Configuration
It is possible to add filter and manipulation rules for the calendar entries. 
All of them can be changed in the [/custom-configuration](/custom-configuration) folder.

To make the changes apply, the container must be rebuilt.

TODO explain that a bit more.

## Future Ideas
 - This service could also be accessed by our website in future. This service aims to filter and prettify dates in such a way, that they can be used for publication. For that the API functionality must be extended a little.
 - Build a GUI to change the custom configurations in a more convenient way, than within the .json files.

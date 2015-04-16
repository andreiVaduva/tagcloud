### Tagcloud backend

###### Short description
&nbsp;&nbsp;&nbsp;&nbsp; Implemented the backend for a sample tagcloud service using twitter sample stream.

###### Tools and languages
* implemented in Python, using Flask framework
* used Redis for incrementing the word counts
* used a Docker container for running Redis
* used a Docker container for running the Python application
* used Docker Compose for putting together the Python application's Docker with the Redis one

###### Environment installation and set-up
* [Install Docker and Compose](https://docs.docker.com/compose/install)
* [Install Docker and Compose on Linux Mint](https://github.com/docker/docker/issues/4578)

###### Build and run
**1.** *Open a terminal console*</br>
**2.** *Go into application's folder*</br>
**3.** *Run the following command*</br>
```
docker-compose up
```
Now, Compose will pull a Redis image, build an image for the Python application's code, and start everything up.
The web app should now be listening on port 5000 on your Docker daemon host.</br>
</br>
**4.** *You can run the application either from another terminal [4.1](#4.1) or from an web browser [4.2](#4.2)*</br>
<a name="4.1">**4.1**</a> *Open another terminal and give one of the following commands:*</br>
* use this command to run the program with default values 5 seconds and 5 words included in tagcloud
```
curl 0.0.0.0:5000
```
</br>
* use this command to run the program with the given number of seconds as parameter and a default value of 5 words included in tagcloud
```
curl 0.0.0.0:5000/post/the_duration_of_the_data_fetch
```
</br>
* use this command to run the program with the given number of seconds as parameter and given number of words included in tagcloud
```
curl 0.0.0.0:5000/post/the_duration_of_the_data_fetch/how_many_words_it_should_include_in_the_tagcloud
```
</br>
*******************************************************************************************************************
**After running the application with one of the above commands you will receive in current terminal the sample stream statistics.</br>Also, in the first terminal (the terminal where you run the docker-compose) you can track the stream evolution, step by step.**
*******************************************************************************************************************
</br>
<a name="4.2">**4.2**</a> *Open an web brouser insert one of the following links:*</br>
* use this link to get the program running results with default values 5 seconds and 5 words included in tagcloud
```
http://0.0.0.0:5000
```
* use this link to get the program running results with the given number of seconds as parameter and a default value of 5 words included in tagcloud
```
http://0.0.0.0:5000/post/the_duration_of_the_data_fetch
```
* use this link to get the program running results with the given number of seconds as parameter and given number of words included in tagcloud
```
http://0.0.0.0:5000/post/the_duration_of_the_data_fetch/how_many_words_it_should_include_in_the_tagcloud
```
</br>
*******************************************************************************************************************
**After running the application with one of the above links you will receive in your web browser the sample stream statistics.</br>Also, in the first terminal (the terminal where you run the docker-compose) you can track the stream evolution, step by step.**
*******************************************************************************************************************
</br>
</br>
##### Useful references:
---
* [Python Documentation](https://www.python.org/doc/)
* [Docker Documentation](http://docs.docker.com/)
* [Redis Documentation](http://redis.io/documentation)
* [Redis-py Documentation](https://redis-py.readthedocs.org/en/latest/)
* [Tweepy Documentation](http://docs.tweepy.org/en/latest/api.html)


import json
import os
import re
import sys
import time
import tweepy
from collections import OrderedDict
from flask import Flask
from redis import Redis
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


# Authentication details
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


app = Flask(__name__)
# redis connection
redis = Redis(host='redis', port=6379)

# list of delimiters for split
delims = '[ .,!?;:_/\n\t\r\-\"\*\^\&\%\(\)\{\}\[\]]'

# read from file the list of stopwords
with open("stopwords.txt") as fin:
    stopwords = [x.strip('\n') for x in fin.readlines()]


class StdOutListener(StreamListener):
    """
    Class that extends StreamListener class.
    """
    def __init__(self, time_out, tagcloud_size, api=None):
        """Constructor.

        @type time_out: Integer
        @param time_out: the duration of the fetch process

        @type tagcloud_size: Integer
        @param tagcloud_size: the number of words it should include
                              in the tagcloud
        """
        super(StdOutListener, self).__init__()
        self.start_time = time.time()
        self.time_out = time_out
        self.tagcloud_size = tagcloud_size
    
    def on_data(self, data):
        # verify if time for streaming passed
        if time.time() - self.start_time < self.time_out:
            # decode stream data
            decoded = json.loads(data)

            # also, convert UTF-8 to ASCII ignoring all bad characters
            tweet_text = decoded['text'].encode('ascii', 'ignore')

            # split tweets text into words and get frequency
            split_text(tweet_text, self.tagcloud_size)

            print "Tweet text:\t   " + tweet_text
            return True
        else:
            return False

    def on_error(self, status):
        print status

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

    def on_disconnect(self):
        if self.running is False:
            return None
        self.running = False


def parse_to_json(lst):
    """
    Parse output list into json objects list
    """
    json_list = []
    for elem in lst:
        # append object to list
        json_elem = {'word': elem[0], 'count': int(elem[1])}
        json_list.append(json_elem)

    # sort object with word first and count after
    sort_order = ['word', 'count']
    ordered_results = [OrderedDict(sorted(item.iteritems(),
    	    key=lambda (k, v): sort_order.index(k))) for item in json_list]

    return ordered_results


def split_text(text, tagcloud_size):
    """
    Split tweet text into words and store words into database
    """
    global tagcloud

    # remove links from text
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    
    # remove numbers from text
    text = re.sub(r'^[0-9]*[0-9]', '', text, flags=re.MULTILINE)

    # split text into words
    words = re.split(delims, text)

    for word in words:
        word = word.lower()
        # verify some corner cases like single letters or empty strings
        if word != 'rt' and word != '' and len(word) != 1:
            # stopwords are not counted
            if not word in stopwords:
                # increment the score of member in the sorted set sorted at key
                # by increment; if member does not exist, it is added with score 1
                redis.zincrby("mySortedSet", word, 1)

    # with all words in mySortedSet, I get the words with the most occurrences
    tagcloud = redis.zrevrange("mySortedSet", 0, tagcloud_size-1, 'WITHSCORES')

    # parse output into json objects
    tagcloud = parse_to_json(tagcloud)
    print 'Round output is: %s\n\n' % redis.zrevrange("mySortedSet", 0,
                                            tagcloud_size-1, 'WITHSCORES')


@app.route('/post/<int:t_stream>/<int:tagcloud_size>')
def time_size_args(t_stream, tagcloud_size):
    """
    Start a twitter sample stream using two given command line arguments:
    t_stream and tagcloud_size.
    """

    # empty the database for counting new values
    redis.flushdb()

    # create a streamListener object
    stream_listener = StdOutListener(t_stream, tagcloud_size)

    # get access on twitter stream
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create a twitter sample stream filtering only english tweets
    stream = Stream(auth, stream_listener, timeout=3)
    stream.sample(languages=['en'])

    # parse the json list for printing the output
    tagcloud_output = json.dumps(tagcloud, indent=4, sort_keys=False)
    return str(tagcloud_output)


@app.route('/post/<int:t_stream>')
def one_argument(t_stream):
    """
    Start a twitter sample stream using a given command line argument
    for t_stream and a default parameter: tagcloud_size = 5
    """

    # empty the database for counting new values
    redis.flushdb()

    # create a streamListener object
    stream_listener = StdOutListener(t_stream, 5)

    # get access on twitter stream
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create a twitter sample stream filtering only english tweets
    stream = Stream(auth, stream_listener, timeout=3)
    stream.sample(languages=['en'])

    # parse the json list for printing the output
    tagcloud_output = json.dumps(tagcloud, indent=4, sort_keys=False)
    return str(tagcloud_output)


@app.route('/')
def no_arguments():
    """
    Start a twitter sample stream using as default parameters:
        t_stream = 5
        tagcloud_size = 5
    """

    # empty the database for counting new values
    redis.flushdb()

    # create a streamListener object
    stream_listener = StdOutListener(5, 5)

    # get access on twitter stream
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create a twitter sample stream filtering only english tweets
    stream = Stream(auth, stream_listener, timeout=3)
    stream.sample(languages=['en'])

    # parse the json list for printing the output
    tagcloud_output = json.dumps(tagcloud, indent=4, sort_keys=False)
    return str(tagcloud_output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


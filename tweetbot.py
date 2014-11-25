import os, oauth2, datetime, time, urllib2, json, tweepy, random

########
# CONSTANTS
########

CONSUMER_KEY = os.environ['HEROKU_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['HEROKU_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['HEROKU_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['HEROKU_ACCESS_SECRET']


class Search(object):

    def __init__(self):
        self.url1 ="https://api.twitter.com/1.1/search/tweets.json"
        self.params = {"oauth_version":"1.0",
                  "oauth_nonce": oauth2.generate_nonce(),
                  "oauth_timestamp":int(time.time())
                  }

        self.consumer = oauth2.Consumer(key=CONSUMER_KEY,
                                   secret=CONSUMER_SECRET)
        
        self.token = oauth2.Token(key=ACCESS_TOKEN,
                             secret=ACCESS_SECRET)

        self.params["oauth_consumer_key"] = self.consumer.key
        self.params["oauth_token"] = self.token.key
        
    def search(self, query, count):
        
        for i in range(1):
            url = self.url1
            self.params["q"] = query
            self.params["count"] = count
            req = oauth2.Request(method="GET", url=url, parameters=self.params)
            signature_method = oauth2.SignatureMethod_HMAC_SHA1()
            req.sign_request(signature_method, self.consumer, self.token)
            headers = req.to_header()
            url = req.to_url()
            try:
                response = urllib2.Request(url)

                data = json.load(urllib2.urlopen(response))
                if data:
                    return data
                else:
                    return False
            except urllib2.HTTPError:
                print "Http error" + str(urllib2.HTTPError.code)
                return False
            
    def favorite_hashtag(self, hashtag_query):
        query = self.search(hashtag_query, 5)
        if query:
            statuses = query['statuses']
            for tweet in statuses:
                try:
                    TWITTER_BOT.create_favorite(tweet['id'])
                    print "SUCCESS status: " + str(tweet['id'])
                    print datetime.datetime.now()
                except tweepy.TweepError:
                    print "favorite failed on status: " + str(tweet['id'])
                    print datetime.datetime.now()

        else:
            return                

############
##############

class API(object):
    def __init__(self):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.secure = True
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    def authenticate(self):
        
        return tweepy.API(self.auth)

#############
#############
   
def mention_new_follower():
    followers = TWITTER_BOT.followers()
    most_recent = followers[0].screen_name

    saved_follower = open("./fixtures/most_recent.txt","r")
    s_f = saved_follower.read()
    saved_follower.close()
    if s_f != most_recent:
        new_saved_follower = open("./fixtures/most_recent.txt","w")
        new_saved_follower.write(most_recent)
        new_saved_follower.close()
        lines = open("./fixtures/msgs_to_followers.txt").read().splitlines()
        mention = "@" + str(most_recent)
        try:
            
            TWITTER_BOT.update_status(mention + " " + random.choice(lines))
            print "successfully mentioned new follower: " + most_recent
            print datetime.datetime.now()
        except tweepy.TweepError:
            print "mention failed on new follower " + most_recent
            print datetime.datetime.now()
    else:
        print "No new followers"
            

if __name__ == "__main__":
    twitter = API()
    TWITTER_BOT = twitter.authenticate()
    favorite = Search()
    while True:
        favorite.favorite_hashtag("#teasontheloose")
        favorite.favorite_hashtag("@TeasontheLoose")
        
    
        time.sleep(14400)

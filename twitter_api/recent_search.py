import requests
import os
import json
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url(query, **kwargs):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if 'next_token' in kwargs:
        tweet_fields = "tweet.fields=attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld"
        url = "https://api.twitter.com/2/tweets/search/recent?query={}&since_id=1346175555675295744&max_results=100&{}&next_token={}".format(
            query, tweet_fields, kwargs.get('next_token')
        )
        return url
    else:
        tweet_fields = "tweet.fields=attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld"
        url = "https://api.twitter.com/2/tweets/search/recent?query={}&since_id=1346175555675295744&max_results=100&{}".format(
            query, tweet_fields
        )
        return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main(query, **kwargs):
    bearer_token = auth()
    if 'next_token' in kwargs:
        url = create_url(query, next_token=kwargs.get('next_token'))
    else:
        url = create_url(query)
    headers = create_headers(bearer_token)
    try:
        json_response = connect_to_endpoint(url, headers)
    except:
        print("Connection error -- pausing 15 seconds then retrying")
        time.sleep(15)
        json_response = connect_to_endpoint(url, headers)

    return json.dumps(json_response, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()

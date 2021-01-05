import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url(user_id):
    # Replace with user ID below
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params(**kwargs):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if 'next_token' in kwargs:
        return {"max_results":100, "tweet.fields": "attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld","start_time":"2020-12-29T05:00:00Z","pagination_token":kwargs.get('next_token')}
    else:
        return {"max_results":100, "tweet.fields": "attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld","start_time":"2020-12-29T05:00:00Z"}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main(user_id, **kwargs):
    bearer_token = auth()
    url = create_url(user_id)
    headers = create_headers(bearer_token)
    if 'next_token' in kwargs:
        params = get_params(next_token = kwargs.get('next_token'))
    else:
        params = get_params()
    json_response = connect_to_endpoint(url, headers, params)
    return json.dumps(json_response, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()

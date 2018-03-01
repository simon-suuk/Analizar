import facebook

"""Publishing post to a 
facebook page"""
def publish_created_post_to_facebook_page():
    api = get_api()
    msg = "Welcome to an Insightful Social Media Management Platform!"
    status = api.put_wall_post(msg)
    return status


def get_api():
    config = {
        "page_id": "353394314773005",
        "access_token": "EAAaCCjExSOwBACUOR9wUZA1RdjOZBPxVY4herrqN7j0RJyKDzq09Tk7HejHpKVPOGjqRDCMJBawuCHzEJAb9LPvVG5Ouf3jGLzPZAvbQG2R2gGciLxig9hRMGQnwVAbiokOv1nlOzmqqKKuBqdfMFT4Idj6Bf5j1ZAMRIWhMYiKOn80y0IE12N9gQnoA14wHFnTQ9jc8RUpcLGxO9iZBAtZCx58hXtKvQFZA1ZAjVMAiIAZDZD"
    }
    graph = facebook.GraphAPI(config['access_token'])
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == config['page_id']:
            page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph

publish_created_post_to_facebook_page()

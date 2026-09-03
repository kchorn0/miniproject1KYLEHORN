import os
import requests

BASE = "https://practice.fhsucyber.com"
# Gets the API token from the computer's environment variables
TOKEN = os.environ.get("PRACTICE_API_TOKEN")

# Who am I?
#print(requests.get(f"{BASE}/api/v1/me", headers=headers).json())
#print()

# Creates a class that will contain all API methods
class PracticeHubClient:
    # Runs when a new PracticeHubClient object is created
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        # Creates the Authorization header using the API token
        self.headers = {"Authorization": f"Bearer {token}"}

    #Handle Errors
    def _handle_error(self, resp):
        # Gets the error details from the API response
        detail = resp.json().get("detail", "Unknown error.")
        # Checks if the API returned a 401 error
        if resp.status_code == 401:
            print(f"Error: Invalid or missing API token. {detail}")
        # Checks if the API returned a 403 error
        elif resp.status_code == 403:
            print(f"Error: You can only edit or delete your own posts. {detail}")
        # Checks if the API returned a 404 error
        elif resp.status_code == 404:
            print(f"Error: Post not found. {detail}")
        # Checks if the API returned a 422 error
        elif resp.status_code == 422:
            print(f"Error: Invalid data. {detail}")
        # Handles any other type of error
        else:
            # Raises the error so Python can report what went wrong
            resp.raise_for_status()            

    #Create
    def create_post(self, title, body="", tags=None):
        # Sends a POST request to the posts endpoint and sends the API token in the request headers
        resp = requests.post(f"{self.base}/api/v1/posts", headers=self.headers,
                             # Sends the title, body, and tags as JSON data
                             json={"title": title, "body": body, "tags": tags or []})
        # Checks if the API request was not successful
        if not resp.ok:
                # Call method
                self._handle_error(resp)
                # Returns None to show that the post was not created
                return None
        return resp.json()

    #Read(List)
    def list_posts(self, mine=False, tag=None):
        # Creates the query parameters for the request
        params = {"mine": mine}
        # Checks if a tag was provided
        if tag:
            # Adds the tag to the query parameters
            params["tag"] = tag
        # Sends a GET request to retrieve posts and sends the query parameters with the request
        resp = requests.get(f"{self.base}/api/v1/posts", headers=self.headers, params=params)
        if not resp.ok:
            self._handle_error(resp)
            return None
        return resp.json()

    # TODO (Mini Project 1): get_post, update_post, delete_post

    #Read
    def get_post(self, post_id):
        # Sends a GET request for the specific post ID
        resp = requests.get(
            f"{self.base}/api/v1/posts/{post_id}",
            # Sends the API token in the request headers
            headers=self.headers
        )

        if not resp.ok:
            self._handle_error(resp)
            return None

        return resp.json()  

    #Update
    def update_post(self, post_id, title=None, body=None, tags=None):
        # Creates an empty dictionary to hold the information we want to update
        data = {}
        # Checks if a new title was provided
        if title is not None:
            # Adds the new title to the update data
            data["title"] = title
        # Checks if a new body was provided
        if body is not None:
            # Adds the new body to the update data
            data["body"] = body
        # Checks if new tags were provided
        if tags is not None:
            # Adds the new tags to the update data
            data["tags"] = tags
        # Sends a PATCH request to update the specific post
        resp = requests.patch(
            f"{self.base}/api/v1/posts/{post_id}",
            # Sends the API token in the request headers
            headers=self.headers,
            # Sends only the information that needs to be updated
            json=data
        )
        # Checks if the API request was not successful
        if not resp.ok:
            # Handles the API error
            self._handle_error(resp)
            # Returns None show the update failed
            return None
        # Converts the response from JSON into Python data and returns it
        return resp.json()

    #Delete
    def delete_post(self, post_id):
        # Sends a DELETE request for the specific post
        resp = requests.delete(
            f"{self.base}/api/v1/posts/{post_id}",
            # Sends the API token in the request headers
            headers=self.headers
        )
        # Checks if the API request was not successful
        if not resp.ok:
            self._handle_error(resp)
            # Returns False to show that the deletion failed
            return False
        # Returns True to show that the post was successfully deleted
        return True 




      
# Checks if this file is being run directly instead of being imported
#Test CRUD ops
if __name__ == "__main__":
    # Checks if the API token was not found
    if not TOKEN:
        # Stops the program and displays an error message
        raise SystemExit("PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2.")
    
    # Creates a PracticeHubClient using the API URL and API token
    client = PracticeHubClient(BASE, TOKEN)

    #List # posts
    everyone = client.list_posts()
    if everyone is None:
        raise SystemExit
    print(f"Posts on the hub: {len(everyone)}")

    #Number posts that are mine
    print(f"posts that are mine: {len(client.list_posts(mine=True))}")


    #Create a new "first" post
    #new_post = client.create_post("Week 3 lab", body="My first created post.")
    #print(f"created post {new_post['id']}: {new_post['title']}")

    # Create
    # Creates a new post with a title, body, and tags
    new_post = client.create_post(
        "Mini Project 1",
        body="Testing my CRUD API client.",
        tags=["python", "api"]
    )
    print(f"Created post {new_post['id']}: {new_post['title']}")

    # Read (Get)
    # Gets the ID of the post that was JUST created
    post_id = new_post["id"]
    # Gets the specific post details using its ID
    post = client.get_post(post_id)
    # Prints the ID and title of the post that was retrieved
    print(f"Read post {post['id']}: {post['title']}")

    # Update
    # Updates the title of the post
    updated_post = client.update_post(
        post_id,
        #Changing the title to this!
        title="Mini Project 1 - Updated"
    )
    # Prints the ID and updated title of the post that was edited
    print(f"Updated post {updated_post['id']}: {updated_post['title']}")

    # Delete
    # Deletes the post using its ID
    client.delete_post(post_id)
    print(f"Deleted post {post_id}")
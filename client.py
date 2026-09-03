import os
import requests

BASE = "https://practice.fhsucyber.com"
TOKEN = os.environ.get("PRACTICE_API_TOKEN")

# Who am I?
#print(requests.get(f"{BASE}/api/v1/me", headers=headers).json())
#print()

class PracticeHubClient:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    #Handle Errors
    def _handle_error(self, resp):
        detail = resp.json().get("detail", "Unknown error.")
        if resp.status_code == 401:
            print(f"Error: Invalid or missing API token. {detail}")
        elif resp.status_code == 403:
            print(f"Error: You can only edit or delete your own posts. {detail}")
        elif resp.status_code == 404:
            print(f"Error: Post not found. {detail}")
        elif resp.status_code == 422:
            print(f"Error: Invalid data. {detail}")
        else:
            resp.raise_for_status()            

    #Create
    def create_post(self, title, body="", tags=None):
        resp = requests.post(f"{self.base}/api/v1/posts", headers=self.headers,
                             json={"title": title, "body": body, "tags": tags or []})
        if not resp.ok:
                self._handle_error(resp)
                return None
        return resp.json()

    #Read(List)
    def list_posts(self, mine=False, tag=None):
        params = {"mine": mine}
        if tag:
            params["tag"] = tag
        resp = requests.get(f"{self.base}/api/v1/posts", headers=self.headers, params=params)
        if not resp.ok:
            self._handle_error(resp)
            return None
        return resp.json()

    # TODO (Mini Project 1): get_post, update_post, delete_post

    #Read
    def get_post(self, post_id):
        resp = requests.get(
            f"{self.base}/api/v1/posts/{post_id}",
            headers=self.headers
        )

        if not resp.ok:
            self._handle_error(resp)
            return None

        return resp.json()  

    #Update
    def update_post(self, post_id, title=None, body=None, tags=None):
        data = {}

        if title is not None:
            data["title"] = title

        if body is not None:
            data["body"] = body

        if tags is not None:
            data["tags"] = tags

        resp = requests.patch(
            f"{self.base}/api/v1/posts/{post_id}",
            headers=self.headers,
            json=data
        )
        if not resp.ok:
            self._handle_error(resp)
            return None

        return resp.json()

    #Delete
    def delete_post(self, post_id):
        resp = requests.delete(
            f"{self.base}/api/v1/posts/{post_id}",
            headers=self.headers
        )

        if not resp.ok:
            self._handle_error(resp)
            return False

        return True 




      

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2.")

    client = PracticeHubClient(BASE, TOKEN)

    everyone = client.list_posts()
    print(f"posts on the hub: {len(everyone)}")

    #new_post = client.create_post("Week 3 lab", body="My first created post.")
    #print(f"created post {new_post['id']}: {new_post['title']}")

    print(f"posts that are mine: {len(client.list_posts(mine=True))}")


    #test del functiona nd error handle
    forbidden_delete = client.delete_post(3)
    print(f"Delete result: {forbidden_delete}")
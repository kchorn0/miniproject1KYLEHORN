# miniproject1KYLEHORN
# INF601 - Advanced Programming in Python
### Kyle Horn
### Mini Project 1

# Practice Hub API Client

A Python command-line client that performs a full create/read/update/delete (CRUD) cycle against the Practice Hub REST API.

## Description

This project is an object-oriented Python client for the Practice Hub API. It authenticates using a bearer token and provides methods to create, read, update, and delete posts.

The client wraps every request with error handling for the four API error cases required by this assignment:

- **401** — missing or invalid API token
- **403** — trying to edit or delete a post that isn't yours
- **404** — the requested post doesn't exist
- **422** — invalid or missing data in the request

Instead of letting these errors crash the program with a raw traceback, `_handle_error()` reads the `detail` message from the API response and prints a clear explanation, and the calling method returns `None` (or `False` for delete) so the program can continue safely.

When run directly, `client.py` demonstrates the full CRUD cycle: it lists existing posts, creates a new post, reads it back by id, updates its title, and finally deletes it — printing the result of each step.

### Dependencies

- Python 3.13 (or any Python 3.x)
- Python libraries: `requests` (see `requirements.txt`)
- A Practice Hub API token

### Installing

1. Clone/download this repository.
2. Install the required package:

```bash
pip install -r requirements.txt
```

3. Set your Practice Hub API token as an environment variable (see below). Do **not** commit your token to the repository.

### Executing program

Set your token in the same terminal window you'll run the script from:


```powershell
# Windows PowerShell
$env:PRACTICE_API_TOKEN = "your-token-here"
```

Then run the client:

```bash
python client.py
```

This will list the posts on the hub, create a new post, read it back, update its title, and then delete it — printing each step as it happens.

If you see `PRACTICE_API_TOKEN is not set`, the environment variable didn't carry into the terminal you're running from — set it again in that window and re-run.

## AI Usage
I used Claude Code to help scaffold the initial PracticeHubClient class structure based on the requirements and code provided in the Blackboard shell. I also used Claude Code to review the API endpoint documentation and help me understand how the required methods should be structured and implemented.

During development, I first implemented the _handle_error() method so that the other API methods could use the same error-handling process. I then used AI assistance to help draft and understand the get_post(), update_post(), and delete_post() methods based on the API documentation and project requirements. AI was also used to generate testing scenarios for the different API error responses so I could verify that each error was being properly detected and handled.

I used ChatGPT as an additional learning resource to explain the project requirements, break the project into manageable steps, and help me understand concepts and code that were unclear to me, especially since this is an online course and I did not have the same opportunity for in-person discussion.

I wrote the main demonstration flow myself and tested the client using my own API token to confirm that the complete CRUD cycle worked as expected. I also separately tested the individual methods through the API's GUI. Throughout the project, I reviewed and modified the AI-assisted code rather than simply accepting it. I commented each line of the completed code to make sure I understood what it does and can explain every method
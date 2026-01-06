Hi! This is how you run the tests in this project and information about how to run them.

**Backend tests**

To run backend tests, from the home directory run "cd backend". Then "pip install -r requirements.txt".

Once you've done that, run "pytest" or "pytest -v" for the verbose version and you'll see all of the backend tests run.

Here's what the tests cover:

- test_ai_service: tests all the functions related to the OpenAI API (without actually testing the API). It makes sure we're parsing the input and output of those functions correctly. I am not testing the OpenAI API because I can do this from user testing on the deployed version and AI models are unpredictable. The "AI responses" are all mocked.

- test_app_integration: This tests all the endpoints of my server to make sure that with mocked data, they return what they're supposed to and behaving predictably. All of the server calls get intercepted so they are fed mock data.

- test_auth_service: This tests the authentication system I have put in place and validating mock tokens, requiring authentication in functions, all without actual auth0 tokens being inputted.

- test_database: This uses the temporary database created by the conftest.py file to check the functions in database.py work properly. It tests sending messages, creating conversations, adding and updating users, getting titles, etc. The database is deleted after the tests in conftest.py

Both the auth_service and ai_service are definitely not perfect because they're working with third party software that is a bit tricky, but the mocks do help verify the underlying code and user testing can test a lot of the rest.

**Frontend tests**

To run frontend tests, from the home directory run "cd frontend". Then "npm install".

Once you've done that, run "npm test" and you'll see all the frontend tests run.

Here's what the tests cover:

- ConfirmationModal: tests everything related to the confirmation popup that happens when people want to delete a conversation. Confirms it doesn't pop up when its not supposed to, it does when it's supposed to, it cancels when people click cancel, X, or off the modal, and deletes it if people click confirm.
- ConversationsList: tests everything related to the conversations list on the left hand of the screen. Tests that the right message appears when there are no convos, that it displays loading when its loading, that conversations appear when they're supposed to. Tests that users clicking on a convo makes it highlight and selects the convo, and tests the date functionality and the title functionality.
- FeedbackPanel: tests everything related to the feedback panel appearing. Tests that the score appears properly, that improvement tips appear, and that an example improved prompt appears.
- apiService: tests the requests from the frontend to the server. Uses a mock axios object to make sure that the apiService.js file calls the appropriate endpoints when it uses different functions, including different use cases like if functions have offsets included or not (pagination feature). Makes sure files can be sent, streaming can be done, and conversations can be deleted.

The tests related to visual components (the first three) use the DOM to determine if things are on the screen or not.

**System testing**

Much of the tests I've described above test different aspects of the system pipeline. I found it difficult in code to test complete system flows due to dependencies on third party software like Auth0 and ChatGPT that required verified tokens or keys in order to work (things that work much easier in a deployed environment). Because of that, most of my system testing involved rigorous testing on the deployed version - this included standard flows like logging in, sending messages, reaching the message cap in a conversation, and lots of prompt quality testing. It also involved testing unexpected user behaviors, like deleting conversations mid feedback or response stream, or deleting a new conversation, or trying to add a ton of files. My user testing also allowed me to do system testing, as my experiment put the tool in the hands of users in order to have them complete the SAT essays they were assigned.

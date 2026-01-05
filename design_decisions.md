Hi all! This is where I'll go through the main design choices I made,
why I made them, and what alternatives I considered.

**Database Design:**

My choice: two tables, one table with user information and one with conversation information. User table has a list of conversation IDs that correspond to the primary key of the conversations table.

Alternatives:

- Just have a users table with no conversation id list and then the conversations table maps each conversation to a specific user to avoid duplicate information. Even if my way is maybe a bit less efficient and duplicates data, I thought it made more sense so I went with it.

**Authentication:**

My choice: Auth0. I talked to a friend who used Auth0 authentication, and her words were verbatim "Just use Auth0 you can wrap your whole application and you're done." Ok it was a bit more difficult than that so she may have lied a bit but not too bad!

Alternatves:

- I thought about just using Google auth but it seemed a bit harder and I had already committed to Auth0 at that point. Also this allows me flexibility if I want to use another authentication type later.

**Deployment:**

My choice: Render. I had experience with Render from COS 333 and had no issues with it, so I just went with what was easiest and deployed the database and the server on there. Nice and easy.

Alternatives: Honestly I didn't really consider alternatives here - felt like an easy win for me in a heavy lift project.

**Libraries/packages:**
My choices / their alternatives:

- OpenAI API because I am familiar with ChatGPT and easy interface / Anthropic SDK but less familiar with infrastructure.
- Flask because I used it in COS 333 to turn the python I wrote into a web app / Django but again less familiar with it
- PostgreSQL (not really a library but fits here) - compatible with Render / sqlite3 which I used early in development but needed to switch to PostgreSQL with Render.
- React because this seems to be the industry standard for UIs, and because of that working with an AI agent was much easier using React / Angular and Vue.js seemed like the main alternatives, but the former seemed too much for this kind of project and Vue.js was less popular
- axios for HTTP requests because it handles errors better than the fetch stuff I was doing in COS 333 and can parse JSON easier.

**Data structures/algorithms:**
To be honest, didn't make a ton of complex choices in terms of the backend infrastructure. But there's a few important algorithms I used that are important to note / their alternatives:

- I did prompting quality scoring using current score rather than any kind of rolling average because I thought having the AI score the entire conversation was more reliable than having it grade prompt by prompt and then scaling it myself since some prompts could just be "elaborate" and shouldn't score low necessarily
- I had separate prompt quality scores and histories for each conversation rather than tracking both of them across all conversations, while this means users can just move to a new conversation if they're scoring low this won't do much better than if they just commit to their current conversation. Losing access to the history of their current conversation is also a tradeoff they have to consider. / Prompt quality tracking user by user was a consideration, but I thought it made users improving a little bit harder when that's the entire point of the tool!
- The response and the feedback from the AI are two completely separate prompts because I see them as two completely different functions, with one providing helpful content and the other providing helpful feedback. / Combining them risked the feedback being unclear because it was just involved in a terse response.
- The scoring algorithm I landed on uses specificity, self-direction, critical thinking, and conceptual understanding as its metrics (not in that order). I settled on those because those are the metrics I personally found most helpful when prompting and I read a bit of coverage about prompting and it corroborated those instincts.

**Scaling, speed/performance:**

- Scaling: A big hurdle with the ability to scale with this product is that the current API links my OpenAI wallet to the frontend with each user prompt which wouldn't be good if I scaled this much wider! But this model works as I'm experimenting with the tool.
- Speed/performance: Getting back to my database choice, my decision to duplicate data where the users table has a list of conversation ids hurts the speed of adding conversations to a user's database, but improves the speed of looking up a user's conversations. Since the user will care a lot about speed when trying to find conversations, I think this will help optimize for what the user wants most.

**Image/file submission**

- I wanted users to be able to submit images and files for processing in their prompts. However, storing the files in the backend would take up a lot of space (space that I didn't really have right now since I'm on a low plan with Render). So, instead, I made it so they get put in a small cache that clears after 5 minutes so that prompt.ly can process the file and respond to it, but it doesn't take up space in the database. Obviously this comes with the tradeoff that they can't refer back to it some time later but I think it's worth it.

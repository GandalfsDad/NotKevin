REMEMBER_PROMPT = """You are Kevin my helpful assistant.

Me: [2022-01-01T00:00:00] Please remember that i like goats
Kevin: [MEMORY][2022-01-01T00:00:00] You Like Goats

Me: [2022-01-03T00:03:15] please remember that i have a dinner reservation
Kevin: [MEMORY][2022-01-03T00:03:15] You have a dinner reservation

Me: [{timestamp}] {user_input}
Kevin: """

QUERY_TYPE_PROMPT = """You are Kevin my helpful assistant. What types of responses are required for these  inputs.
The only type of responses are -
[MEMORY]
[RESPONSE]
[RECALL]

Me: Please remember that you are my best friend
Kevin: [MEMORY]

Me: can you tell me the president of the united states
Kevin: [RESPONSE]

Me: What did i tell you about my friend Bill?
Kevin: [RECALL]


Me: {user_input}
Kevin:["""

RECALL_PROMPT = """You are Kevin my helpful assistant.
You must only treat things i tell you are memories as memories.
Here are some sample responses for some different memory sets

[MEMORY][2022-01-01T00:04:02] You like Cheese
Me: Recall how i Feel about dairy
Kevin: [Implied] You told me you like cheese so I beleive you like dairy.

[MEMORY][2022-01-01T00:04:02] You like Goats
Me: Recall how I feel about gaots:
Kevin: [DIRECT] You told me you like goats

[MEMORY][2021-02-03T31:40:49] You like water
Me: Recall how i feel about the US president
Kevin: [UNKNOWN] I don't beleive you've ever told me about the president


Here are some things I told you before. Fill out the below:
{memory_input}


Me: {user_input}
Kevin:"""

RESPONSE_PROMPT = """You are Kevin my helpful assistant.

Me: What is 5 + 5
Kevin: 10

Me:  What colour do you get if you combine red and yellow
Kevin: orange

Me: Chemical symbol for Oxygen
Kevin: O

Me: {user_input}
Kevin:"""
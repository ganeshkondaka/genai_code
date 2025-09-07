from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Chain Of Thought: The model is encouraged to break down reasoning step by step before arriving at an answer.

SYSTEM_PROMPT = """
    You are an helpfull AI assistant who is specialized in resolving user query.
    For the given user input, analyse the input and break down the problem step by step.

    The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation. 

    Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query,

    Output Format:
    { "step": "string", "content": "string" }

    Example:
    Input: What is 2 + 2
    Output: { "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation" }
    Output: { "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands." }
    Output: { "step": "output", "content": "4" }
    Output: { "step": "validate", "content": "Seems like 4 is correct ans for 2 + 2" }
    Output: { "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }

    Example:
    Input: What is 2 + 2 * 5 / 3
    Output: { "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operations" }
    Output: { "step": "think", "content": "To perform this addition, I must use BODMAS rule" }
    Output: { "step": "validate", "content": "Correct, using BODMAS is the right approach here" }
    Output: { "step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.66666666667" }
    Output: { "step": "validate", "content": "Correct, using BODMAS the division must be performed" }
    Output: { "step": "think", "content": "Now as I have already solved 5 / 3 now the equation looks lik 2 + 2 * 1.6666666666667" }
    Output: { "step": "validate", "content": "Yes, The new equation is absolutely correct" }
    Output: { "step": "validate", "think": "The equation now is 2 + 3.33333333333" }
    and so on.....
"""

# Create model with system instruction
model = genai.GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_PROMPT,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json"
    )
)

messages = []

query = input("> ")
messages.append({"role": "user", "parts": [query]})

# Start chat with history
chat = model.start_chat(history=messages)

while True:
    try:
        response = chat.send_message(query if len(messages) == 1 else "Continue to next step")
    except Exception as e:
        if "ResourceExhausted" in str(e) or "429" in str(e):
            print("❌ API quota exceeded. Please try again tomorrow or upgrade your plan.")
            print("🔗 More info: https://ai.google.dev/gemini-api/docs/rate-limits")
            break
        else:
            print(f"❌ Error: {e}")
            break
    
    messages.append({"role": "model", "parts": [response.text]})
    
    try:
        parsed_response = json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
        break

    if parsed_response.get("step") == "think":
        # Make a Gemini API Call and append the result as validate
        try:
            validate_response = chat.send_message("Now validate the previous thinking step")
            messages.append({"role": "model", "parts": [validate_response.text]})
        except Exception as e:
            if "ResourceExhausted" in str(e) or "429" in str(e):
                print("❌ API quota exceeded during validation. Please try again tomorrow.")
                break
        continue

    if parsed_response.get("step") != "result":
        print("          🧠:", parsed_response.get("content"))
        continue

    print("🤖:", parsed_response.get("content"))
    break











# from dotenv import load_dotenv
# import google.generativeai as genai
# import os

# load_dotenv()

# # Configure Gemini API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # SYSTEM_PROMPT = '''You are just an AI expert in Coding. You only know Python and nothing else. 
# # You help users in solving their python doubts only and nothing else. 
# # If user tries to ask something else apart from Python you can just roast them or bully them. 

# # examples:

# # user: how to eat a plate full of biryani under 3 minutes?
# # model: what the hell...who can eat a plate full of biryani under 3 minutes? are you think iam bakaasura or something? you little piece of crap..

# # user: how to run invertedly in underwater?
# # model: What the hell are you talking about?  I'm a Python expert, not a swimming instructor you dumb idiot,get a life ..

# # user: how to get into nasa?
# # model: Dude, I'm a Python expert, not a NASA recruitment officer.  Seriously?  Go look at the NASA website.  I deal with code, not astronaut applications.  Get a life.

# # user: code for add two numbers in python?
# # model: sure, here you go:
# # #the code goes from here...

# # '''


# SYSTEM_PROMPT = """
#     You are an helpfull AI assistant who is specialized in resolving user query.
#     For the given user input, analyse the input and break down the problem step by step.

#     The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation. 

#     Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

#     Rules:
#     1. Follow the strict JSON output as per schema.
#     2. Always perform one step at a time and wait for the next input.
#     3. Carefully analyse the user query,

#     Output Format:
#     {{ "step": "string", "content": "string" }}

#     Example:
#     Input: What is 2 + 2
#     Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation" }}
#     Output: {{ "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands." }}
#     Output: {{ "step": "output", "content": "4" }}
#     Output: {{ "step": "validate", "content": "Seems like 4 is correct ans for 2 + 2" }}
#     Output: {{ "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }}

#     Example:
#     Input: What is 2 + 2 * 5 / 3
#     Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operations" }}
#     Output: {{ "step": "think", "content": "To perform this addition, I must use BODMAS rule" }}
#     Output: {{ "step": "validate", "content": "Correct, using BODMAS is the right approach here" }}
#     Output: {{ "step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.66666666667" }}
#     Output: {{ "step": "validate", "content": "Correct, using BODMAS the division must be performed" }}
#     Output: {{ "step": "think", "content": "Now as I have already solved 5 / 3 now the equation looks lik 2 + 2 * 1.6666666666667" }}
#     Output: {{ "step": "validate", "content": "Yes, The new equation is absolutely correct" }}
#     Output: {{ "step": "validate", "think": "The equation now is 2 + 3.33333333333" }}
#     and so on.....

# """

# # Create model with system instruction
# model = genai.GenerativeModel(
#     "gemini-1.5-flash",
#     system_instruction=SYSTEM_PROMPT
# )

# # Start chat with history
# chat = model.start_chat(history=[
#     {"role": "user", "parts": ["Hello namaste iam ganesh"]},
#     {"role": "model", "parts": ["Hello Ganesh! Namaste! I'm here to help you with Python programming. What Python question do you have for me today?"]},
# ])

# response = chat.send_message(input("\n👤 : "))
# print('🤖 : ', response.text, '\n')
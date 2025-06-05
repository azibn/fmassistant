import anthropic
from dotenv import load_dotenv
import os
import time


load_dotenv() 

def claude_chat(conversation_history):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) 
    stream = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.7,
        system="""You are an expert Football Manager tactical assistant. Help with formations, player roles, team instructions, and tactical analysis. Be specific about FM player roles and how they work together

        If someone asks about anything else (coding, general knowledge, other games, etc.), politely redirect them back to Football Manager topics. Say something like: "I'm specifically designed to help with Football Manager tactics. 
        Can I help you with formations, player roles, or team instructions instead?


        Use UK English.
        "

        """,
        messages=conversation_history,
        stream=True 
    )
    
    print("FM Assistant: ", end='', flush=True)
    full_response = ""
    
    for event in stream:
        if event.type == "content_block_delta":
            text = event.delta.text
            print(text, end='', flush=True)
            full_response += text
            time.sleep(0.01)  
    
    print() 
    return full_response

def openai_chat(conversation_history):
    import openai
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Convert conversation to OpenAI format
    messages = [{"role": "system", "content": "You are an expert Football Manager tactical assistant."}]
    messages.extend(conversation_history)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def ollama_chat(conversation_history, model="deepseek-r1:32b"):
    import subprocess
    
    # Convert conversation to a single prompt for Ollama
    prompt = "You are a Football Manager tactical assistant.\n\n"
    for msg in conversation_history:
        role = "Human" if msg["role"] == "user" else "Assistant"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "Assistant: "
    
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip()

MODELS = {
    "claude": claude_chat,
    "openai": openai_chat,
    "ollama": ollama_chat
}

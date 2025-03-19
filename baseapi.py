import openai

openai.api_key = "YOUR_API_KEY"

def generate_response(prompt, model="gpt-4", temperature=0.7, max_tokens=150):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message['content'].strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        ai_response = generate_response(user_input)
        print(f"AI: {ai_response}")
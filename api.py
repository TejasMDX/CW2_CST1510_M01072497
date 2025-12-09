from google import genai

#"AIzaSyDifL7gRxDlVqD95nlXyhXEdPYCPrR_L5s"
client = genai.Client(api_key="AIzaSyDifL7gRxDlVqD95nlXyhXEdPYCPrR_L5s")

print("Gemini with Memory. Type 'quit' to exit.\n")

messages = [
    {
        "role": "user",
        "parts":[
            {
                "text": "Your name is now Tom"
            }
        ]
    },
]

while True:
    user_input= input("You: ")
    if user_input.lower() == "quit":
        break
    messages.append({"role":"user","parts":[{"text":user_input}]})

    response = client.models.generate_content_stream(
        model = "gemini-2.5-flash",
        contents = messages,
    )

    full_reply = ""
    for chunk in response:
        full_reply += chunk.text
        print(full_reply,end = "")

    messages.append({"role":"model","parts":[{"text":full_reply}]})
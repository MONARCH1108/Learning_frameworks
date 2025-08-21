import ollama

context = """
You are an assistant with access to the following information only:

1. Monarch is a tech company started by Abhay, focusing on AI, automation, and web technologies.
2. Monarch's flagship project is a multimodal search engine that can understand text and images.
3. Monarch is also building AI tools for Twitter bots, personal productivity, and educational apps.
4. All answers should be strictly based on this context. If the answer is not in the context, respond with: "Sorry, I don't have that information."
"""

question = input("Enter Your Question?: ")
response = ollama.chat(
    model="deepseek-r1:1.5b",
    messages=[
        {"role":"system","content":f"ans based on {context}"},
        {"role":"user","content":f"{question}"},
    ],
    stream=True
)

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)

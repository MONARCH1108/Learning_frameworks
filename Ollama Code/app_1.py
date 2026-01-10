import ollama


response = ollama.chat(
    model="deepseek-r1:1.5b",
    messages=[
        {"role":"user", "content":"who is mark"},
    ],
    stream=True
)

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)
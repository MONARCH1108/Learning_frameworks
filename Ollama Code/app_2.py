import ollama

response = ollama.generate(
    model="deepseek-r1:1.5b",
    prompt="who is a phycopath?",
)

print(response)
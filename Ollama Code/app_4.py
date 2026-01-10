import ollama

context = """
Samantha Ruth Prabhu (born 28 April 1987) is an Indian actress who works predominantly in Telugu and Tamil films. One of South India's highest-paid actresses,[2][3][4] Samantha is the recipient of several accolades, including four Filmfare Awards South, two Nandi Awards and a Tamil Nadu State Film Award.

After a brief stint as a model while pursuing a degree in commerce, Samantha made her acting debut in the Telugu romance film Ye Maaya Chesave (2010), winning the Filmfare Award for Best Female Debut – South. She became the second actress to win both the Filmfare Award for Best Actress – Tamil and Best Actress – Telugu in the same year, for her performances in the 2012 films Neethaane En Ponvasantham and Eega, respectively. Over the next few years, she played the leading lady in top-grossing androcentric films such as Dookudu (2011), Seethamma Vakitlo Sirimalle Chettu (2012), Attarintiki Daredi (2013), Kaththi (2014), Theri (2016), 24 (2016), Mersal (2017), and Rangasthalam (2018).

Her performance in A Aa (2016) won Samantha her fourth Filmfare Award, and she gained further praise for her performances in Mahanati (2018), Super Deluxe (2019), and Majili (2019), and the Amazon Prime Video thriller series The Family Man (2021). The last of these earned her a Filmfare OTT Award. Following two critical and commercial failures,[5][6] she starred in the action series Citadel: Honey Bunny (2024). Samantha is also the founder of a charitable trust Pratyusha Support.
"""
prompt = f"""
1. you are an search assist
2. ans only from the context given and do not add you own knowladge
3. do not think too much 

Context:
\"\"\"{context}\"\"\"
"""
question = input("ask ur question?  : ")

response = ollama.chat(
    model="deepseek-r1:1.5b",
    messages=[
        {"role":"system","content":prompt},
        {"role":"user","content":question},
    ],
    stream=True
)

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)
from openai import OpenAI

client = OpenAI(
    base_url = "https://api.scaleway.ai/c98de2b2-feb7-4780-a578-4c5276194bf4/v1",
	api_key = "8b23f64f-b2e5-453d-a23f-3fcf56dfd598"
)

def askQuestion(question, language, gender):
    response = client.chat.completions.create(
        model="mistral-nemo-instruct-2407",
        messages=[
            { "role": "system", "content": "You are a useful AI assistant. You will ask me back the question I am giving it to you. Give me the questions in the correct language, with the proper gender if needed." + "Do it in " + language + ". You are talking to a " + gender },
            { "role": "user", "content": question },
        ],
        max_tokens=512,
        temperature=0.6,
        top_p=0.95,
        presence_penalty=0,
        stream=True,
    )
    return (response)

def printResponse(response):
    for chunk in response:
        if chunk.choices and chunk.choices[-1].delta.content:
            print(chunk.choices[-1].delta.content, end="", flush=True)

i = 0;
question = "ais-je de la fatigue lors d'un effort physique ?"
language = "english"
gender = "female"
response = askQuestion(question, language, gender)
printResponse(response)

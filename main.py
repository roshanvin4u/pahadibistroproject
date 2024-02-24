import openai

OPENAI_API_KEY = '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'

openai.api_key = OPENAI_API_KEY

messages = []
messages.append( 
    {"role": "user", "content": "Categorize Beans, Apples, Cauliflower into Vegetables and Fruits."}, 
) 
chat = openai.ChatCompletion.create( 
    model="gpt-3.5-turbo", messages=messages 
) 
reply = chat.choices[0].message.content 
print(f"{reply}")
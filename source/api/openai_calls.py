from openai import OpenAI


client = OpenAI(api_key='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')

print("----- standard request -----")
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        },
    ],
)
print(completion.choices[0].message.content)

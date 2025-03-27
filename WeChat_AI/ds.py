# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="<your deepseek api_keys>", base_url="https://api.deepseek.com")
def get_response(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个温柔的男神"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    prompt = "你是谁？"
    response = get_response(prompt)
    print(response)

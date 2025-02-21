from openai import OpenAI
from config.settings import settings

APIKEY = settings.APIKEY
BASEURL = settings.BASEURL
MODELNAME = settings.MODELNAME

client = OpenAI(
  base_url = BASEURL,
  api_key = APIKEY,
)

def request_ds(prompt, abi):
  completion = client.chat.completions.create(
    # extra_headers={
      # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
      # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    # },
    model=MODELNAME,
    messages=[
      {
        "role": "system",
        "content": prompt+abi
      }
    ]
  )
  return completion.choices[0].message.content
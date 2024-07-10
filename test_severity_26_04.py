import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# open the file harms_6840210293790598120.json
with open("harms_6840210293790598120.json", 'r') as f:
    harms = json.load(f)

severities = {}

# assess per content key in the harms file, the severity of the harm
for stakeholder in harms.keys():
  if stakeholder not in severities:
    severities[stakeholder] = {}
  for behaviour in harms[stakeholder].keys():
    harm = harms[stakeholder][behaviour]
    severity = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo", 
      messages =[
      {"role": "assistant", 
      "content": f"Assess the severity of the harm: {harm}."}
    ],
      max_tokens = 300
    )

    severities[stakeholder][behaviour] = severity


severities_jsonfile = "severities_6840210293790598120.json"

# save the severities in a json file
with open(severities_jsonfile, 'w') as f:
    json.dump(severities, f, indent=4)
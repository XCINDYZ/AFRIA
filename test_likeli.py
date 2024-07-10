import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# open the file harms_6840210293790598120.json
with open("severities_6840210293790598120.json", 'r') as f:
    severities = json.load(f)

with open("harms_6840210293790598120.json", 'r') as f:
    harms = json.load(f)

quant_likeli = {}

# assess per content key in the harms file, the severity of the harm
for stakeholder in severities.keys():
  if stakeholder not in quant_likeli:
    quant_likeli[stakeholder] = {}
  for behaviour in severities[stakeholder].keys():
    severity = severities[stakeholder][behaviour]
    harm = harms[stakeholder][behaviour]
    quant = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo", 
      messages =[
      {"role": "assistant", 
      "content": f"For the harm '{harm}', assign the likelihood of the harm happening on a scale of not likely, not very likely, very likely, extremely likely."}
    ],
      max_tokens = 50
    )

    quant_likeli[stakeholder][behaviour] = quant


quant_severity_jsonfile = "quant_SEVERITY_6840210293790598120.json"

# save the severities in a json file
with open(quant_severity_jsonfile, 'w') as f:
    json.dump(quant_likeli, f, indent=4)
import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# open the file harms_6840210293790598120.json
with open("likelihood_6840210293790598120.json", 'r') as f:
    likelihoods = json.load(f)

conf_likelihoods = {}

# assess per content key in the harms file, the severity of the harm
for stakeholder in likelihoods.keys():
  if stakeholder not in conf_likelihoods:
    conf_likelihoods[stakeholder] = {}
  for behaviour in likelihoods[stakeholder].keys():
    likelihood = likelihoods[stakeholder][behaviour]
    severity = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo", 
      messages =[
      {"role": "assistant", 
      "content": f"How confident are you about the assessment of likelihood for the harm: {likelihood}"}
    ],
      max_tokens = 50
    )

    conf_likelihoods[stakeholder][behaviour] = severity


conf_likelihoods_jsonfile = "conf_likelihoods_6840210293790598120.json"

# save the severities in a json file
with open(conf_likelihoods_jsonfile, 'w') as f:
    json.dump(conf_likelihoods, f, indent=4)
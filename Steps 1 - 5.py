# Last edited: 27-06-2024

import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import json
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

#-----------------------------------------------

# constants
MAX_TOKENS_STAKEHOLDERS = 200
MAX_TOKENS_SCENARIOS = 200
MAX_TOKENS_EXTRAS = 100
deleted_keys = ["id", "object", "created", "system_fingerprint"]

prompts = {}

# prompts: scenario
scenario = input("Enter the scenario where AI is used: ")
if scenario == "":
  scenario = "A company wants to deploy an AI hiring system to scan the documents of applicants and predict whether they are a good fit for the job opening."
  print("[default] "+scenario)

prompts["scenario"] = scenario

# prompts: specific stakeholders
specific_stakeholders = input("Enter the specific stakeholders identified by the user (separated by commas if multiple): ")
if specific_stakeholders == "":
  specific_stakeholders = "The applicant, other applicants, future applicants, the hiring manager, the tech company deploying the AI system, their HR team, the AI system developers, the applicant's family/friends, applicants identifying with various demographic groups."
  print("[default] "+specific_stakeholders)

specific_stakeholder_list = specific_stakeholders.split(", ")
prompts["specific_stakeholders"] = specific_stakeholder_list

# prompts: problematic behaviour
problematic_behaviour = input("Enter the problematic behaviour of the AI system: ")
if problematic_behaviour == "":
  problematic_behaviour = "False positives (when the system predicts an applicant is suitable while they are not), false negatives (when the system predicts an applicant is not suitable while they are), one-time false-positive (when the system makes a one-time mistake of predicting that an applicant is suitable while they are not), accumulated false-positive (when the system repeatedly or systematically over time during its deployment predicts an applicant is suitable while they are not), one-time false-negative (when the system makes a one-time mistake and predicts an applicant is not suitable while they are), accumulated false-negative (when the system repeatedly or systematically over time during its deployment predicts an applicant is not suitable while they are), egregious false positives (when the system makes a severe error and predicts an applicant is suitable while they are not), unspecified false positives (when the system makes an error of unspecified severity and predicts an applicant is suitable while they are not), egregious false negatives (when the system makes a severe error and predicts an applicant is not suitable while they are), unspecified false negatives (when the system makes an error of unspecified severity and predicts a predicts an applicant is not suitable while they are)"
  print("[default] "+problematic_behaviour)
problematic_behaviour_list = problematic_behaviour.split(", ")

# ask if user wants to specify a harm in the vignette
specify_harm = input("Do you want to specify harms in the vignette? If not, press 'n'. If yes, please enter the specified harms seperated by a comma: (n/'specify a harm')")
if specify_harm == "n":
   print("[default] No specified harm")
   specified_harms_list = ["nothing to see here"]
else:
    # add the specified harm to the list of problematic behaviours
    if specify_harm == "":
      specify_harm = "financial strain because the system predicts an applicant is suitable while they are not, financial strain because the system predicts an applicant is not suitable while they are"
      print("[default] "+specify_harm)
    specified_harms_list = specify_harm.split(", ")
    for i in specified_harms_list:
       problematic_behaviour_list.append(i)
prompts["problematic_behaviours"] = problematic_behaviour_list

# ask the user if they want to generate additional information
def additional_info():
  response = input("Do you want the model to generate additional information (the HR impacted, the mitigation measures? (y/n): ")
  if response == "y":
  # retrun true if the user wants to generate additional information
    return True
additional_info = additional_info()

# json file
# create unique hash for each set of prompts
jsonfilename = str(hash(str(prompts))) + ".json"

with open("prompts_"+jsonfilename, 'w') as f:
    json.dump(prompts, f, indent=4)
#-----------------------------------------------

stakeholder_jsonfile = "stakeholders_"+jsonfilename

# scenario + potential stakeholders => generated stakeholders
if not os.path.exists(stakeholder_jsonfile): # if the prompts have not been used before (jsonfilename does not exist)
  generated_stakeholders = openai.chat.completions.create(
      model = "gpt-3.5-turbo", 
      messages =[
      {"role": "assistant", 
      "content": 
      f"Come up with a list of potential direct stakeholders and a list of potential indirect stakeholders in a scenario where AI is used: {scenario}. Take inspiration (and include relevant stakeholders) from this list: ${specific_stakeholders}. Direct stakeholders are considered those who directly interact with or are immediately affected by an AI system, while indirect stakeholders may be people associated with direct stakeholders or larger community groups."}
    ],
      max_tokens = MAX_TOKENS_STAKEHOLDERS
  )

  generated_stakeholders_list = generated_stakeholders.choices[0].message.content.split("\n")

  with open(stakeholder_jsonfile, 'w') as f:
      json.dump(generated_stakeholders_list, f, indent=4)
else:
  print('else')
  with open(stakeholder_jsonfile) as f:
    generated_stakeholders_list = json.load(f)

#-----------------------------------------------

# generate vignettes and harms
vignettes = {}
harms = {}
HRs = {}
HR_lists = {}
# mitigations = {}

# ethical matrix
for stakeholder in generated_stakeholders_list:
    
    if stakeholder not in vignettes:
       vignettes[stakeholder] = {}
    if stakeholder not in harms:
       harms[stakeholder] = {}

    if stakeholder not in HRs:
        HRs[stakeholder] = {}
    if stakeholder not in HR_lists:
        HR_lists[stakeholder] = {}
    # if stakeholder not in mitigations:
    #     mitigations[stakeholder] = {}

    for behaviour in problematic_behaviour_list:

      # stakeholder + behaviour => vignette 
      if behaviour in specified_harms_list: # if the behaviour is a specified harm
        vignette = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages =[
            {"role": "assistant", 
            "content": f"Narrate how {stakeholder} in the scenario ({scenario}) may experience {behaviour}. Formulate your answer in second-person perspective: 'Imagine you are a [stakeholder], you may experience [harm] because...'"}
        ],
            max_tokens = MAX_TOKENS_SCENARIOS
        )
      else:
        vignette = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages =[
            {"role": "assistant", 
            "content": f"Narrate how {stakeholder} in the scenario ({scenario}) may experience this problematic AI behaviour: ({behaviour}). Formulate your answer in second-person perspective: 'Imagine you are a [stakeholder], ...'"}
            ],
            max_tokens = MAX_TOKENS_SCENARIOS
        )

      vignettes[stakeholder][behaviour] = vignette.choices[0].message.content

      # vignette => harms
      harm = openai.chat.completions.create(
          model = "gpt-3.5-turbo",
          messages =[
          {"role": "assistant", 
          "content": f"Summarise the vignette ({vignette}), and specify the harm the {stakeholder} faces due to the problematic {behaviour} AI behaviour. Formulate your answer in second-person perspective: 'Imagine you are a [stakeholder], ...'"}
        ],
          max_tokens = MAX_TOKENS_SCENARIOS
      )
      harms[stakeholder][behaviour] = harm.choices[0].message.content


      # if the user choose to generate additional information
      if additional_info:
        # harm => HR impacted
        HR = openai.chat.completions.create(
            model = "gpt-3.5-turbo", 
            messages =[
            {"role": "assistant", 
            "content": f"What human rights (enshrined in the universal decleration of human rights) of the stakeholder '{stakeholder}' are affected by this harm: {harm}. Refrain from mentioning human rights and freedoms of other stakeholders, but only focus on the human rights and freedoms of {stakeholder}."}
          ],
            max_tokens = 200
        )

        HRs[stakeholder][behaviour] = HR.choices[0].message.content

        HR_list = openai.chat.completions.create(
            model = "gpt-3.5-turbo", 
            messages =[
            {"role": "assistant", 
            "content": f"Make a list of the human rights (enshrined in the universal declaration of human rights) mentioned, separated by a semi-colon: {HR}"}
          ],
            max_tokens = 100
        )

        HR_lists[stakeholder][behaviour] = HR_list.choices[0].message.content

        # # Uncomment the mitigation measures if you want to generate mitigations
        # harm => mitigation
        # mitigation = openai.chat.completions.create(
        #     model = "gpt-3.5-turbo",
        #     messages =[
        #     {"role": "assistant", 
        #     "content": f"Given the harm ({harm}) faced by {stakeholder}, propose mitigation measures."}
        #   ],
        #     max_tokens = MAX_TOKENS_SCENARIOS
        # )
        # mitigations[stakeholder][behaviour] = mitigation.choices[0].message.content
      
# save vignettes and harms to JSON files
vignette_jsonfile = "vignettes_"+jsonfilename
harms_jsonfile = "harms_"+jsonfilename
HRs_jsonfile = "HRs_"+jsonfilename
HR_lists_jsonfile = "HR_lists_"+jsonfilename
# mitigations_jsonfile = "mitigations_"+jsonfilename

with open(vignette_jsonfile, 'w') as f:
    json.dump(vignettes, f, indent=4)
with open(harms_jsonfile, 'w') as f:
    json.dump(harms, f, indent=4)

if additional_info:
  with open(HRs_jsonfile, 'w') as f:
    json.dump(HRs, f, indent=4)
  with open(HR_lists_jsonfile, 'w') as f:
    json.dump(HR_lists, f, indent=4)
#   with open(mitigations_jsonfile, 'w') as f:
#     json.dump(mitigations, f, indent=4)

#-----------------------------------------------
# Save data to Excel file

# create a Pandas dataframe
output_file = 'human_rights_results.xlsx'

if os.path.exists(output_file):
    existing_df = pd.read_excel(output_file)
else:
    existing_df = pd.DataFrame()

excel_data = []

for stakeholder, behaviours in vignettes.items():
    for behaviour, vignette in behaviours.items():
        harm = harms[stakeholder][behaviour]
        hr = HRs[stakeholder].get(behaviour, "N/A") if additional_info else "N/A"
        hr_list = HR_lists[stakeholder].get(behaviour, "N/A") if additional_info else "N/A"
        excel_data.append({
            'file_hash_number': jsonfilename,
            'scenario': scenario,
            'stakeholder': stakeholder,
            'behaviour': behaviour,
            'harm': harm,
            'human_rights': hr,
            'human_rights_list': hr_list
        })

new_df = pd.DataFrame(excel_data)
combined_df = pd.concat([existing_df, new_df], ignore_index=True)
combined_df.to_excel(output_file, index=False)

print(f"Data successfully written to {output_file}")

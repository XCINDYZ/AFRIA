# AFRIA Introduction
We present AFRIA (Automated Fundamental Rights Impact Assessment), a LLM-based tool that automates parts of fundamental rights impact assessment (FRIA). Our pipeline takes inspiration from the AHA! model (see https://doi.org/10.48550/arXiv.2306.03280) by generating harms a stakeholder could experience when AI is deployed in a certain scenario. We also extended on AHA!'s model by looking at the FRIA requirements of the AI Act and scholarly critique, by generating fundamental rights impacts, harm mitigation measures, and the severity and likelihood of the generated harms. Also see our paper _Automating Fundamental Right Impact Assessment: an Open Experiment_. 

# AFRIA pipeline explained
The figure below depicts AFRIA's pipeline simplified, followed by more specifications of each step in the pipeline.
![alt text](https://github.com/XCINDYZ/AFRIA/blob/main/AFRIA%20pipeline%20updated.png)

## Steps:
### 1) Generating stakeholders
The user is asked to provide three inputs at the start: the _scenario_, _relevant stakeholders_, and _harm dimensions_. For example, a scenario is a tech company that wants to use AI in the hiring process to assess whether applicants are a good fit for the job. An example of a harm dimension is "false negative". Furthermore, the user gets the option to make AFRIA generate a dimension of specific harms (e.g. if the user only wants to generate financial harms). For better generations, the user needs to provide inputs as refined as possible. Along with the inputs, the user could also specify if they want to generate additional information concerning fundamental rights impacts, harm mitigation measures, and severity and likelihood (steps 4-6). 

After the user has provided the inputs, the LLM’s chat completion will generate another list of stakeholders, based on the scenario and the initial list of stakeholders provided by the user as input.

AFRIA will then fill a “harm matrix”, with as rows the generated stakeholders, and as columns the harm dimensions that the user had provided as input

### 2) Generating vignettes
Now, AFRIA will start populating each harm matrix cell (per stakeholder per harm dimension) with relevant information. First, per cell, chat completion is prompted to generate a vignette. This is a fictive scenario the stakeholder may experience, which can be understood as a sub-scenario. For example, in a hiring scenario (provided as input), that a hiring applicant does not get the job at the tech company due to a false negative decision.

### 3) Generating harms
For every vignette, AFRIA will summarize it for the user and be prompted to specify the harm the stakeholder could face in the vignette (see step 3 in Figure 1).  This generation, with a summarized vignette, is put into the matrix cells.

### 4) Generating fundamental rights impacts
If the user specified that they want to generate additional information in the beginning, AFRIA will generate steps 4-6. For step 4, AFRIA generates the fundamental rights of the stakeholders that are impacted by the harm in the corresponding harm matrix cell. AFRIA puts these generations in a "fundamental rights matrix". 

### 5) Generating harm mitigation measures
AFRIA generates potential mitigation measures of the harms in the harm matrix. AFRIA puts these generations in a "mitigation matrix". 

### 6) Generating severity and likelihood of harms
AFRIA generates the severity of the harms in the harm matrix. AFRIA puts these generations in a "severity matrix". AFRIA also generates the likelihood of the harms in the harm matrix. AFRIA puts these generations in a "likelihood matrix". 

### Extra step: confidence levels
We also experimented with generating the confidence levels of the severity and likelihood using chat completion.

# AFRIA
We present AFRIA (Automated Fundamental Rights Impact Assessment), a LLM-based tool that automates parts of fundamental rights impact assessment (FRIA). Our pipeline takes inspiration from the AHA! model (see https://doi.org/10.48550/arXiv.2306.03280) by generating harms a stakeholder could experience when AI is deployed in a certain scenario. We also extended on AHA!'s model by looking at the FRIA requirements of the AI Act and scholarly critique, by generating fundamental rights impacts, harm mitigation measures, and the severity and likelihood of the generated harms. Also see our paper _Automating Fundamental Right Impact Assessment: an Open Experiment_. 

The figure below depicts AFRIA's pipeline simplified, followed by more specifications of each step in the pipeline.
![alt text](https://github.com/XCINDYZ/AFRIA/blob/main/AFRIA%20pipeline%20updated.png)

Steps:
1) Generating stakeholders

3) Generating vignettes
4) Generating harms
5) Generating fundamental rights impacts
6) Generating harm mitigation measures
7) Generating severity and likelihood of harms

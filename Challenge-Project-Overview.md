---

> ## Challenge Advisor: Update & Finalize Your Project Overview
>
> > 💡 **These grey text instructions are just for you, the team's Challenge Advisor; please delete them once you have completed the steps below.**
>
> We've pre-populated this Challenge Project Overview page — which is what will be shared with your Break Through Tech student team in August — using the details from your submission form. You should have received an email inviting you to join this repo as a Collaborator, enabling you to add files and make edits.
> 
> In order for your project to be finalized and assigned to a team, please:
> 1. **Review all sections below** and update or expand any content as needed, making sure to address the SME Feedback in the section immediately below. Look for square brackets to find the places below that require additional inputs from you (e.g., "About [Company / Org Name]").
> 2. **Add your dataset** to the [data folder](data) in this repo.
> 3. **Close the Issue assigned to you in this repo** to let us know that you have made your edits and the overview page is ready for final review. You can do this by going to the _Issues_ tab in the top left section of the menu above, add a comment that says "CA review complete", and click the button to Close the Issue. 
>
> If you're unfamiliar with how to edit a page like this in GitHub, check out [this tutorial](https://ubc-lib-geo.github.io/gis-workshop-waml-template/content/handson/edit-readme.html) for a quick overview (start with step 2 and only edit this page), and [this guide](https://ubc-lib-geo.github.io/gis-workshop-waml-template/content/markdown.html) on how to use Markdown to compose text.
>
>
> ❌ Remember that this is a public repo. Do NOT include: Proprietary data, PII, API keys, credentials, or anything confidential.

---

## 📋 BTT Internal Evaluation Notes
*(This section is for BTT staff and CAs only — remove before sharing with students)*

### Technical Vetting
| Check | Status | Notes |
| :--- | :--- | :--- |
| Python Compatibility | 🟢 | Stack is fully compatible with the standard PyData ecosystem (pandas, scikit-learn, numpy). Keras is included in TensorFlow/Colab defaults. |
| Data Readiness | 🟡 | Data requires significant normalization; IPUMS/BLS/O*NET schemas are notoriously non-trivial to join and will require substantial ETL work. |
| Resource Check | 🟢 | Well within free-tier Colab limits; dataset size is manageable. |

### Internal Scores
- **Student Fit Score:** 8/10
- **Technical Depth Score:** 7/10
- **Overall Recommendation:** REVISE

### Advisor Feedback Draft
This project offers a high-value analytical exploration into labor economics and AI impact. To ensure success, first, pivot the Keras model requirement to a Random Forest or XGBoost baseline, which provides superior feature importance transparency for tabular data. Second, implement a strict 'Merge-First' milestone by week 3 to mitigate the risk of schema-mapping failure. I recommend moving forward with these constraints to ensure a robust, high-impact final deliverable.

---

# Do AI Job-Risk Indices Agree?

**Company / Org:** Swytch  
**Challenge Advisor:** Julie Young, julie@swytch.careers  
**Program:** Break Through Tech AI Studio - Fall 2026  

---

## 🏢 About Swytch
Swytch is an innovative organization dedicated to providing data-driven career guidance and professional development insights. By analyzing complex labor market trends, the team empowers individuals to navigate the evolving workforce landscape with clarity and confidence.

---

## 🎯 The Challenge
### Project Summary
In this project, you will use several public indexes that score how exposed each U.S. occupation is to AI (the Felten-Raj-Seamans AIOE, the Eloundou GPT-exposure scores, and the Frey-Osborne automation estimates), joined to the O*NET occupational database, and machine learning methods (rank-correlation analysis, clustering, regression, feature-importance methods, and a Keras model), to measure how much these AI-risk rankings actually agree, and to work out what kinds of jobs they disagree about most. This helps SWYTCH know which AI-risk signals are solid enough to use in career guidance and which are too shaky to trust.

### Success Criteria
One clean, reproducible table that combines the different AI-risk indices. Clear numbers on where they agree and where they diverge. A grouping of occupations by risk profile. A model showing which job features explain the disagreements. And a plain writeup of what it all means for trusting any single AI-risk number.

### Stretch Goals
- Free option: add more indices (Webb; the Brynjolfsson-Mitchell-Rock machine-learning-suitability scores), or build an interactive dashboard that lets users explore the merged data.
- Optional API-based add-on (TBD, only if API access is later funded): have an LLM produce its own occupation risk ratings and compare them to the established indices.
  
### Project Milestones
Use these milestones to guide your work. Your team will create a GitHub Projects board to track tasks within each milestone.

| Month | Milestone | Key Activities |
|---|---|---|
| September | Data Standardization & Exploration | Gather and standardize each index. Line them up to the same occupation codes using public crosswalks, merge them into one table, and explore each one. |
| October | Index Agreement & Occupation Clustering | Measure how much the indices agree (rank correlations and concordance). Group occupations by their risk profiles. |
| November | Modeling Disagreements & Validation | Model what drives the disagreements, using occupational features (skills, tasks, job zone, work context). See which features matter most. Add a Keras model. Optionally, check the indices against actual BLS employment projections. |

> **Note for the team:** Please create a GitHub Projects board in this repository to break these milestones into weekly tasks. Go to the **Projects** tab → **New project** → Choose **Board** → Add columns for each month.

---

## 📊 Dataset
**Name and Source:** O*NET, CPS, BLS OES, and BLS Employment Projections
**Format:** CSV/Tabular  
**Size:** under 1gb  
**Location:** https://cps.ipums.org, https://www.onetcenter.org/database.html, https://www.bls.gov/oes, https://www.bls.gov/emp/tables/occupational-separations-and-openings.htm)

### Key Details
- [Brief description of what's in the data]
- [Any known limitations or preprocessing needed]
- [Link to data dictionary or documentation, if available]
  
---

## 🛠️ Suggested Approach

**ML Problem Type:** Regression, Clustering, Deep Learning / Neural Networks  

**Recommended Libraries:**
- [e.g., pandas, scikit-learn, TensorFlow, Hugging Face]

**Evaluation Metrics:**
- [e.g., Accuracy, Precision/Recall, RMSE, BLEU score]

---

## 📚 Resources to Get Started

The following resources will help your team understand the problem space and potential technical approaches for this project:

**Background Reading:**
- [e.g., Link to an article or blog post about the problem domain]
- [e.g., Link to an industry report or case study]

**Technical Tutorials:**
- [e.g., Link to a free tutorial on the ML technique(s) involved]
- [e.g., Link to documentation for a key library or tool]

**Code Examples:**
- [e.g., Link to a relevant GitHub repo]
- [e.g., Link to a sample implementation or starter code]

**Other:**
- [Links to any additional resources — e.g., papers, videos, podcasts, etc.]

*Feel free to explore beyond these, and share anything interesting you find with me!*

---

## 🤝 How We'll Work Together

**Official check-ins:** During our biweekly 45-minute AI Studio Lab Section meeting block (2nd and 4th week of every month)

 **Other ways to reach out to me with questions:** 
* [e.g., Your team's channel within Break Through Tech’s Discord space]
* [e.g., Email; please copy your teammates and AI Studio Coach]
* [e.g., Request a team check-in on Zoom]
* [Note: I will aim to respond within 48 hours. Please reach out to your AI Studio Coach with urgent questions.]

> 💡 **Challenge Advisor: Please update the above based on your availability and preference. If you are not able to answer questions or meet with fellows outside of the biweekly Lab Section check-ins, simply write in "N/A (only available during the official check-in times)"**

**Recommended free coding / collaboration tools**
* […]
* […]

---

## 🚀 Getting Started

1. **Review this overview document** and note any questions for our first meeting
2. **Begin reviewing the dataset** using the link above
3. **Read the GitHub Projects documentation** [here](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)

I’m excited to work with you!

---

## ❓ Questions?

Please bring any questions to our first meeting during the week of August 24th (Break Through Tech’s Bridge to Studio - Session C). 

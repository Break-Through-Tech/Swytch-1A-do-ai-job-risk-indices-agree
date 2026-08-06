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
This project aims to synthesize disparate AI-risk indices—including the AIOE, GPT-exposure, and Frey-Osborne estimates—to evaluate their consistency in predicting labor market disruption. By joining these metrics with O*NET occupational data and applying machine learning techniques, the team will identify which job characteristics drive consensus or disagreement among models. The final output will enable Swytch to provide more reliable, evidence-based career advice to users in an era of rapid technological change.

### Success Criteria
One clean, reproducible table that combines the different AI-risk indices. Clear numbers on where they agree and where they diverge. A grouping of occupations by risk profile. A model showing which job features explain the disagreements. And a plain writeup of what it all means for trusting any single AI-risk number.

### Project Milestones
Use these milestones to guide your work. Your team will create a GitHub Projects board to track tasks within each milestone.
| Month | Milestone | Key Activities |
|-------|-----------|----------------|
| September | Data Ingestion, Harmonization & Baseline Correlation Analysis | • Ingest and link multi-source public datasets (O*NET, IPUMS CPS, BLS OES) using SOC occupational crosswalks.<br>• Standardize and normalize published AI job-risk/exposure indices (e.g., Felten AIOE, OpenAI/Eloundou, Webb, Frey & Osborne).<br>• Perform Exploratory Data Analysis (EDA) and compute pairwise correlation metrics (Pearson/Spearman) across index scores. |
| October | Divergence Modeling & Demographic Disparity Analysis | • Analyze index agreement and variance across demographic groups (gender, race, age, education level), wage tiers, and geographic regions.<br>• Train clustering and decision tree/regression models to identify specific task profiles and occupational features driving high index disagreement.<br>• Measure variance metrics and flag outlier occupations where AI exposure estimates conflict most. |
| November / December | Interpretability, Interactive Dashboard & Capstone Deliverables | • Perform feature importance analysis (e.g., SHAP) to isolate specific O*NET work activities and skills causing index divergence.<br>• Build an interactive Streamlit dashboard allowing users to search occupations, compare multi-index risk profiles, and visualize demographic distributions.<br>• Finalize clean, reproducible GitHub repository, final analytical report, and executive presentation deck. |

### Stretch Goals
* **Composite Risk Meta-Index:** Develop an ensemble/weighted composite AI risk score that harmonizes divergent index methodologies based on underlying task-level O*NET attributes.
* **Labor Market Trend Projection:** Integrate BLS 10-year occupational projection data to evaluate whether high index divergence correlates with projected employment shifts and job separations.
* **Dynamic LLM Task Exposure Evaluator:** Build an interactive sandbox tool that leverages an LLM to evaluate AI exposure for emerging or custom job titles based on user-entered task descriptions.

> **Note for the team:** Please create a GitHub Projects board in this repository to break these milestones into weekly tasks. Go to the **Projects** tab → **New project** → Choose **Board** → Add columns for each month.

---

## 📊 Dataset
**Name and Source:** O*NET, CPS, BLS OES, and BLS Employment Projections (https://cps.ipums.org, https://www.onetcenter.org/database.html, https://www.bls.gov/oes, https://www.bls.gov/emp/tables/occupational-separations-and-openings.htm)  
**Format:** CSV/Tabular  
**Size:** under 1gb  
**Location:** Standard public repository links provided.

### Key Details
- The project requires intensive schema matching across cross-walk tables to align O*NET SOC codes with BLS and researcher-specific occupational classifications. Teams must prioritize handling missing values in specific indices to ensure the final joined dataset maintains statistical integrity.

---

## 🛠️ Suggested Approach
**ML Problem Type:** Regression & Clustering  
**Recommended Libraries:**
- rank-correlation analysis
- clustering
- regression
- feature-importance methods
- and a Keras model
**Evaluation Metrics:** Concordance measures, Mean Squared Error (MSE) for regression tasks, and silhouette scores for occupational clustering.

---

## 📚 Resources to Get Started
The following resources will help your team understand the problem space and potential technical approaches for this project:
**Background Reading:**
- Review the methodology sections of the Felten-Raj-Seamans AIOE paper and the Eloundou et al. GPT-exposure study.
**Technical Tutorials:**
- Consult the scikit-learn documentation for feature importance and clustering workflows.
**Code Examples:**
- Refer to the Pandas documentation for handling multi-index merges and relational data joins.

---

## 🤝 How We'll Work Together
**Check-ins:** During our biweekly 60-min AI Studio Lab Section meeting block (2nd and 4th week of every month)  
**Communication:** Email and Slack (details provided in onboarding)  
**Response time:** 24–48 hours for non-urgent inquiries.  
**Recommended Tools:**
- **Coding:** Google Colab Free Tier  
- **Collaboration:** GitHub, Notion  
- **Virtual Meetings:** Zoom, Google Meet  

---

## 🚀 Getting Started
1. **Review this overview document** and note any questions for our first meeting.
2. **Begin reviewing the dataset** using the link provided in the Dataset section.
3. **Read the GitHub Projects documentation** [here](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects).

I'm excited to work with you!

---

## ❓ Questions?
Please bring any questions to our first meeting during the week of August 24th (Break Through Tech's Bridge to Studio - Session B).

# 📁 COVID Clinical Research - PDF Papers

## Instructions

Place your 5 IEEE papers related to COVID-19 clinical research in this folder.

### Recommended Topics:
- COVID-19 symptoms and diagnosis
- Treatment protocols and therapies
- Vaccine development and efficacy
- Long COVID and post-acute sequelae
- Epidemiology and transmission studies

### File Naming Suggestions:
- `covid_symptoms_diagnosis_2020.pdf`
- `covid_treatment_protocols.pdf`
- `covid_vaccine_efficacy.pdf`
- `covid_long_term_effects.pdf`
- `covid_transmission_study.pdf`

## Finding IEEE Papers

1. Visit: https://ieeexplore.ieee.org/
2. Search for: "COVID-19 clinical" or "COVID-19 diagnosis" or "COVID-19 treatment"
3. Filter by: Open Access (if possible)
4. Download PDFs and place them here

## Note

- The system will automatically process all `.pdf` files in this folder
- You can add more than 5 papers for better coverage
- After adding papers, run: `python data_ingestion.py` to process them
- Sample clinical data CSV is already included in the parent folder

## Current Files

This folder should contain your PDF papers. The system includes sample CSV data for testing even without PDFs.

**Status:** Waiting for your IEEE papers...

Once you add papers, this folder will contain:
```
covid_paper_1.pdf
covid_paper_2.pdf
covid_paper_3.pdf
...
```

---

**Important:** Do not place any files directly in the parent `data/covid/` folder. Only PDFs should go in this `pdfs/` subfolder.

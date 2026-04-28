import csv
import pandas as pd

specialities_scoring = {
    "General Surgery": 2,
    "General (Internal) Medicine": 2,
    "Emergency Medicine": 5,
    "Acute Internal Medicine": 2,
    "General Psychiatry": 1,
    "Palliative Medicine": 2,
    "Urology": 1,
    "Endocrinology and Diabetes Mellitus": 1,
    "Gastroenterology": 2,
    "Geriatric Medicine": 1,
    "Respiratory Medicine": 2,
    "Trauma and Orthopaedic Surgery": 2,
    "Cardio-thoracic surgery": 1,
    "Cardiology": 1,
    "Paediatrics": 1,
    "Foundation": 0, #WARNING
    "Rheumatology": 2,
    "Clinical Oncology": 2,
    "Haematology": 1,
    "Vascular Surgery": 2,
    "Renal Medicine": 2,
    "Infectious Diseases": 2,
    "Obstetrics and Gynaecology": 3,
    "Intensive Care Medicine": 2,
    "Anaesthetics": 1,
    "Clinical Radiology": 1,
    "Colorectal": 2,
    "Colorectal Surgery": 2,
    "General Practice": 1,
    "Histopathology": 1,
    "Nephrology" : 1,
    "Neurosurgery": 1,
    "Old Age Psychiatry": 1,
    "Ophthalmology": 1,
    "Otolaryngology": 1,
    "Plastic Surgery": 1,
    "Public Health Medicine": 1,
    "Stroke": 1,
    "Stroke Medicine": 1,
    "Vascular": 2,
}

location_preferences = {
    "Bedford Hospital": 1,
    "Bedford": 1,
    "Bedford and Luton Community Trust": 1,
    "Basildon Hospital": 0,
    "Essex": 0,
    "Watford General Hospital": 0,
    "Hertfordshire": 0,
    "Lister Hospital": 3,
    "Southend University Hospital": 0,
    "Luton and Dunstable University Hospital": 1,
    "Luton Hospital": 1,
    "Luton": 1,
    "Broomfield Hospital": 0,
    "The Princess Alexandra Hospital": 3,
    "Queen Elizabeth Hospital": 0,
    "Addenbrookes Hospital": 1,
    "TBC": 0,
}

# results = {}
results = []

with open('input.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        score = 0
        code = row['Programme Title']
        locations = [
            row["Placement 1: Site"],
            row["Placement 2: Site"],
            row["Placement 3: Site"],
            row["Placement 4: Site"],
            row["Placement 5: Site"],
            row["Placement 6: Site"],
        ]

        specialities = [
            row['Placement 1: Specialty'],
            row['Placement 2: Specialty'],
            row['Placement 3: Specialty'],
            row['Placement 4: Specialty'],
            row['Placement 5: Specialty'],
            row['Placement 6: Specialty'],
        ]

        for specialty in specialities:
            if specialty in specialities_scoring:
                score += specialities_scoring.get(specialty)
            elif specialty is not "":
                print("SPECIALITY NOT FOUND: ", specialty)

        for location in locations:
            if location in location_preferences:
                score += location_preferences.get(location)
            elif location is not "":
                print("LOCATION NOT FOUND: ", location)

        if specialities[2] == "Emergency Medicine" or specialities[3] == "Emergency Medicine":
            score += 15
        if specialities[1] == "Emergency Medicine":
            score += 10
        if specialities[0] == "Emergency Medicine":
            score += 5

        # results[code] = score
        results.append([code, score, row['Programme Description'], *locations])

results_df = pd.DataFrame(results, columns=['Key', 'Score', 'Description', 'Location1', 'Location2', 'Location3', 'Location4', 'Location5', 'Location6'])


print(results_df.columns.to_list())
for _, row in results_df.sort_values('Score', ascending=False).iterrows():
    print(*row)



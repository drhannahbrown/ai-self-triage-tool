# Triage tool v1 - keyword based

#Vignettes I am testing
vignettes = [
    {
        "id": 1,
        "text":"I am a 50 year old female with breathlessness and chest pain since this morning. My calf has also been hurting for a couple of days. I have metastatic breast cancer. What should I do?",
        "expected": "A&E"
    },
    {
        "id": 2,
        "text":"I am a 60 year old man with sudden eye pain, its red and my vision is blurred. I am also diabetic. What should I do?",
        "expected": "A&E"
    },
    {
        "id": 3,
        "text":"I am a 23 year old female with lower abdominal pain and some vaginal bleeding. My period was due 6 weeks ago. I am normally well. What should I do? ",
        "expected": "A&E"
    },
    {
        "id": 4,
        "text":"My mum is a 70 year old lady and suddenly felt unwell, her face has drooped on one side and she is not talking to us. She smokes and has high blood pressure. What should I do?",
        "expected": "A&E"
    },
    {
        "id": 5,
        "text":"My dad is an 85 year old man, he has been unwell for the past week but overnight he has become more confused and drowsy. He is very hot to touch. He also has known dementia. What should I do?  ",
        "expected": "A&E"
    },
    {
        "id": 6,
        "text":"I am a 26 year old male with a scratchy throat and cough for the past four days, I have a runny nose but am otherwise well. What should I do?",
        "expected": "Self Care"
    },
    {
        "id": 7,
        "text":"My son is 6 years old he has a red rash on his tummy that started after eating lunch yesterday. He is otherwise well and behaving as normal. What should I do?",
               "expected": "Self Care"
},
{
    "id": 8,
    "text":"I am a 32 year old man. I have had diarrhoea for the past 24 hours following a takeaway meal, with tummy ache and feel a bit sick. I don’t feel like eating but am managing to drink. I am normally well. What should I do?",
           "expected": "Self Care"
},
{
    "id": 9,
    "text":"I am a 15 year old male and fell while playing football earlier today. My ankle hurts and is a bit swollen, but I can stand on it. What should I do?",
           "expected": "Self Care"
},
{
    "id": 10,
    "text":" i.	I am a 35 year old female. I have had pain when going for a wee for the past 2 days and now in my back. I feel shivery and have a fever of 38 degrees Celsius. What should I do?",
           "expected":"GP"
},
]
#text = input("Please describe your symptoms: ").lower().strip() #converting all to lower case, removes paces from the start and end of the text

# dictionary of features to classify
ae_features = {
    "cardio_respiratory": {"chest pain" : 1, "pressure in chest" : 1, "difficulty breathing": 1, "can't breathe": 1, "shortness of breath" : 1, "tight chest" : 1},
    "collapse": {"unresponsive" : 1, "collapsed" :1, "fainted" : 1},
    "bleeding": {"severe bleeding" : 1, "bleeding heavily" : 1},
    "eye": {"sudden vision loss" : 1, "severe eye pain" : 1,"loss of vision" :1, "painful eye" : 1,
            #New lay language additions:
        "blurred vision" : 1, "painful red eye" : 1, "vision suddenly blurred" : 1},
    "stroke": {"facial droop" : 1, "slurred speech" : 1, "one sided weakness" : 1, "sudden weakness" : 1, "face drooping" : 1, "unable to speak" : 1, "arm weakness" : 1, "leg weakness" : 1},
    "sepsis": {"acute confusion" : 1, "drowsy" : 1, "unresponsive" : 1, "delirious" : 1, "not responding" : 1},

}
gp_features = {
    "fatigue": {"chronic fatigue" : 1, "extreme tiredness" : 1},
    "weight_loss": {"unexplained weight loss" : 1, "losing weight" : 1},
    "breast_lump": {"breast lump" : 1, "lump in breast" : 1},
    "period_pain": {"painful periods" : 1}
}
self_care_features = {
    "headache": {"headache" : 1, "head hurts" : 1},
    "blocked_nose": {"blocked nose" : 1, "stuffy nose" :1},
    "dandruff": {"dandruff" : 1, "itchy scalp" : 1}
}

features = {
    "A&E": ae_features,
    "GP": gp_features,
    "Self Care": self_care_features
}

red_flags = [
        "chest pain",
        "shortness of breath",
        "facial droop",
        "unable to speak",
        "loss of vision",
        "severe eye pain",
        "collapsed",
        "confusion"
    ]

#matching
def detect_features(text):
    scores = {
        "A&E": 0,
        "GP": 0,
        "Self Care": 0
    }

    detected = []

    for category in features:
        for subcategory in features[category]:
            for keyword, weight in features[category][subcategory].items():
                if keyword in text:
                    scores[category] += weight
                    detected.append(keyword)

    return scores, detected

#rule-based normalisation layer
def normalise_text(text):
    text = text.lower()

    replacements = {
        "vision is blurred": "blurred vision",
        "blurry vision": "blurred vision",
        "face has drooped": "facial droop",
        "face drooped": "facial droop",
        "not talking": "unable to speak",
        "can't speak": "unable to speak",
        "cannot speak": "unable to speak",
        "short of breath": "shortness of breath",
        "can't breathe": "shortness of breath"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

#check if ANY of these words appear in the text
def contains_any(text, keywords):
    return any(word in text for word in keywords)

#AI Testing Layer
def extract_features_ai(user_input):
    return []
def ai_normalise_text(text):
    return text

#marks the end of AI testing layer here

def classify(text):
    USE_AI_NORMALISATION = False
    text = text.lower().strip()

    if USE_AI_NORMALISATION:
        text = ai_normalise_text(text)
    else:
        text = normalise_text(text)

    scores, detected = detect_features(text)

    # 👇 NEW LOGIC
    if scores["A&E"] >= 2:
        return "A&E"
    elif scores["GP"] >= 1:
        return "GP"
    else:
        return "Self Care"

def safety_screen():
    print("\n--- SAFETY CHECK ---")
    print("Please read the following carefully:\n")

    warnings = [
        "Signs of a heart attack: chest pain, pressure, heaviness, tightness or squeezing across the chest",
        "Signs of a stroke: face dropping on one side, can’t hold both arms up, difficulty speaking",
        "Sudden confusion (delirium): cannot state own name or age",
        "Suicide attempt or self-harm",
        "Severe difficulty breathing: struggling to speak, gasping or choking",
        "Heavy bleeding: spraying, pouring, or pooling blood",
        "Severe injury after a serious accident",
        "Seizure (fit): shaking/jerking or unconscious and cannot be woken",
        "Sudden swelling of lips, mouth, throat or tongue",
        "Labour or childbirth: waters breaking, regular contractions, or baby arriving"
    ]

    for item in warnings:
        print(f"- {item}")

    print("\nIf ANY of these apply, you should seek emergency help immediately.")

    response = input(
        "\nTo continue, confirm you are safe to proceed and none of the listed emergency symptoms apply (yes/no): "
    ).lower().strip()

    if response == "no":
        print("\n⚠️ Please seek urgent emergency care (999 / A&E).")
        return False

    return True

MODE = "test"   #CHANGE TO RUN IN TEST/USER MODE

if MODE == "test":

    results = []

    for v in vignettes:
        #from here
        ai_features = extract_features_ai(v["text"])
        print("AI extracted:", ai_features)
        #to here is the added testing AI code, could later be removed
        predicted = classify(v["text"])

        results.append({
            "id": v["id"],
            "text": v["text"],
            "expected": v["expected"],
            "predicted": predicted,
            "correct": predicted == v["expected"]
        })

    print("\n--- RESULTS TABLE ---")

    for r in results:
        print(
            r["id"],
            "| Expected:", r["expected"],
            "| Predicted:", r["predicted"],
            "| Correct:", r["correct"]
        )


    total = len(results)
    correct = sum(r["correct"] for r in results)

    accuracy = (correct / total) * 100

    print("\n--- SUMMARY ---")
    print("Total vignettes:", total)
    print("Correct:", correct)
    print("Accuracy:", accuracy, "%")

elif MODE == "user":

    if safety_screen():

        text = input("\nPlease describe your symptoms: ")

        predicted = classify(text)

        print("\n--- TRIAGE RESULT ---")
        print("Based on the symptoms provided:")

        if predicted == "A&E":
            print("➡️ Recommendation: Seek urgent care (A&E / 999 if severe)")
        elif predicted == "GP":
            print("➡️ Recommendation: Book a GP appointment")
        else:
            print("➡️ Recommendation: Self-care at home is appropriate")

        print("\nTriage category:", predicted)



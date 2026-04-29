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
    "cardio_respiratory": {"chest pain" : 3, "pressure in chest" : 3, "tight chest" : 3, "difficulty breathing": 3, "can't breathe": 3, "shortness of breath" : 3, "tight chest" : 3},
    "collapse": {"unresponsive" : 3 , "collapsed" :3, "fainted" : 2},
    "bleeding": {"severe bleeding" : 3, "bleeding heavily" : 3},
    "eye": {"sudden vision loss" : 3, "severe eye pain" : 3,"loss of vision" :3, "painful eye" : 2,
            #New lay language additions:
        "blurred vision" : 3, "painful red eye" : 3, "vision suddenly blurred" : 3, "sudden vision loss" : 3},
    "stroke": {"facial droop" : 3, "slurred speech" : 3, "one sided weakness" : 3, "sudden weakness" : 3, "face drooping" : 3, "unable to speak" : 2, "arm weakness" : 3, "leg weakness" : 3},
    "sepsis": {"acute confusion" : 3, "drowsy" : 3, "unresponsive" : 3, "delirious" : 3, "not responding" : 3},

}
gp_features = {
    "fatigue": {"chronic fatigue" : 2, "extreme tiredness" : 2},
    "weight_loss": {"unexplained weight loss" : 2, "losing weight" : 2},
    "breast_lump": {"breast lump" : 2, "lump in breast" : 2},
    "period_pain": {"painful periods" : 2}
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

#matching
def detect_features(text):
    scores = {
        "A&E": 0,
        "GP": 0,
        "Self Care": 0
    }

    for category in features:
        for subcategory in features[category]:
            for keyword, weight in features[category][subcategory].items():
                if keyword in text: #flexible word match
                    scores[category] += weight

    return scores
#sematic normalisation layer
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

def has_red_flag(text):
    red_flags = [
        "chest pain",
        "shortness of breath",
        "facial droop",
        "unable to speak",
        "loss of vision",
        "severe eye pain",
        "collapsed",
        "unresponsive"
    ]
    return any(flag in text for flag in red_flags)


#check if ANY of these words appear in the text
def contains_any(text, keywords):
    return any(word in text for word in keywords)


def classify(text):
    text = normalise_text(text.lower().strip())

    # STEP 1: emergency override (ONLY true red flags)
    if has_red_flag(text):
        return "A&E"

    # STEP 2: scoring for everything else
    scores = detect_features(text)
    return max(scores, key=scores.get)


# decision logic
#ae_detected = detect_features(ae_features, text)
#gp_detected = detect_features(gp_features, text)
#self_detected = detect_features(self_care_features, text)

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


results = []

for v in vignettes:
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
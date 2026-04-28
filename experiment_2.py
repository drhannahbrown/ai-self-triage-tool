# =========================================================
# 1. NORMALISATION
# =========================================================

def normalise(text):
    return text.lower().strip()


# =========================================================
# 2. RED FLAG (A&E TRIGGER LAYER)
# =========================================================
# These represent time-critical / potentially life-threatening symptoms

RED_FLAGS = [
    # neurological
    "facial droop",
    "unable to speak",
    "one sided weakness",
    "arm weakness",
    "leg weakness",

    # respiratory / cardiac
    "chest pain",
    "shortness of breath",
    "can't breathe",
    "can’t breathe",

    # collapse / critical
    "collapsed",
    "unresponsive",

    # sensory red flags
    "loss of vision",
    "sudden vision loss",
    "severe eye pain"
]


def has_red_flag(text):
    return any(flag in text for flag in RED_FLAGS)


# =========================================================
# 3. LOW-RISK PATTERN LAYER (NOT A&E)
# =========================================================
# These represent common self-limiting presentations

LOW_RISK_PATTERNS = [
    "cough",
    "runny nose",
    "sore throat",
    "cold",
    "diarrhoea",
    "vomiting",
    "mild pain",
    "stuffy nose"
]


def is_low_risk(text):
    matches = sum(pattern in text for pattern in LOW_RISK_PATTERNS)
    return matches >= 2


# =========================================================
# 4. FINAL CLASSIFIER
# =========================================================

def classify(text):

    text = normalise(text)

    # Step 1: safety override
    if has_red_flag(text):
        return "Go to A&E"

    # Step 2: clear low-risk cases
    if is_low_risk(text):
        return "A&E not required"

    # Step 3: uncertain cases default to safe side
    return "Go to A&E"

# ============================
# INTERACTIVE INPUT
# ============================

if __name__ == "__main__":

    print("=== Simple Triage Tool v1 ===")


    user_input = input("Describe your symptoms: ")

    result = classify(user_input)

    print("\n--- RESULT ---")
    print("Decision:", result)

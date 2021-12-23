import random

dragon = ("dragon", "dragun")
jackbox = ("jackbox", "boxjack")
jackbox_count = 2


def dragon_response():
    letter_count = random.randint(6, 14)
    letters = (("m", "M"), ("h", "H"))
    response = random.choice(letters[1])
    for x in range(letter_count):
        response += random.choice(letters[0])
    return response


def jackbox_response():
    global jackbox_count
    jackbox_count += 1
    if (jackbox_count % 3) == 0:
        responses = ("Ah yes, I see someone say Jackbox", "Jackbox huh", ":fire:", ":zap:", ":four_leaf_clover:",
                     "Finally another mention of jackbox", "Jackbox yes", "Jackbox jackbox jackbox", ":mailbox_with_no_mail:",
                     "Jackbox jackbox yes", "Did somebody say jackbox?", "Yas", "More jackbox", "Yeeeeeeee",
                     ":regional_indicator_j: :regional_indicator_a: :regional_indicator_c: :regional_indicator_k: :regional_indicator_b: :regional_indicator_o: :regional_indicator_x:")
        response = random.choice(responses)
        return response

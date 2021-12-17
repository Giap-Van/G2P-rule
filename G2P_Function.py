import os, json
from collections import defaultdict

def load_g2p_consonants():
    p2g = defaultdict(list)
    with open('G2P_consonants.json','r') as f:
        p2g = json.load(f)
    return p2g

def load_g2p_vowels():
    p2g = defaultdict(list)
    with open('G2P_vowels.json','r') as f:
        p2g = json.load(f)
    return p2g

def load_g2p_falling_tone():
    p2g = defaultdict(list)
    with open('G2P_falling_tone.json','r') as f:
        p2g = json.load(f)
    return p2g

def load_g2p_curve_tone():
    p2g = defaultdict(list)
    with open('G2P_curve_tone.json','r') as f:
        p2g = json.load(f)
    return p2g

def load_g2p_broken_tone():
    p2g = defaultdict(list)
    with open('G2P_broken_tone.json','r') as f:
        p2g = json.load(f)
    return p2g

def load_g2p_rising_tone():
    p2g = defaultdict(list)
    with open('G2P_rising_tone.json','r') as f:
        p2g = json.load(f)
    return p2g

def load_g2p_drop_tone():
    p2g = defaultdict(list)
    with open('G2P_drop_tone.json','r') as f:
        p2g = json.load(f)
    return p2g

def G2P_word(word, consonants, vowels, g2p_consonants, g2p_vowels, fallings, curves, brokens, risings, drops):
    # print(consonants)
    # print(vowels)    
    p_word = []
    id = 0

    for initial in consonants:
        if word.startswith(initial):
            id += len(initial)
            phoneme = g2p_consonants[initial]
            if initial == 'gi':
                if (id > len(word)) or (id <= len(word) and word[id] == 'ê'):
                    p_word.append('zi')
                else:
                    p_word.append(phoneme[0])
            else:
                p_word.append(phoneme[0])
            break
    
    flat1 = 1
    while flat1 == 1:
        flat2 = -1
        for vowel in vowels:
            if word.find(vowel, id) == id:
                flat2 = 1
                id += len(vowel)
                phoneme = g2p_vowels[vowel]
                if vowel == 'a':
                    if (id <= len(word)-1) and (word[id] == 'u' or word[id] == 'y'):
                        p_word.append(phoneme[1])
                    elif (id <= len(word)-2) and ((word[id] == 'n' and word[id+1] == 'h') or (word[id] == 'c' and word[id+1] == 'h')):
                        p_word.append(phoneme[2])
                    else:
                        p_word.append(phoneme[0])
                elif vowel == 'o':
                    if (id <= len(word)-1) and (word[id] == 'c'):
                        p_word.append(phoneme[1])
                    elif (id <= len(word)-2) and (word[id] == 'n' and word[id+1] == 'g'):
                        p_word.append(phoneme[1])
                    else:
                        p_word.append(phoneme[0])
                else:
                    p_word.append(phoneme[0])
                break
        if flat2 == -1:
            flat1 = -1
    
    for final in consonants:
        if word.endswith(final):
            phoneme = g2p_consonants[final]
            if final == 'ch':
                if (id - 1 >= 0) and (word[id-1] == 'i' or word[id-1] == 'ê' or word[id-1] == 'a'):
                    p_word.append(phoneme[1])
                else:
                    p_word.append(phoneme[2])
            elif final == 'nh':
                p_word.append(phoneme[1])
            elif final == 'ng':
                if (id - 1 >= 0) and (word[id-1] == 'u' or word[id-1] == 'o' or word[id-1] == 'ô'):
                    p_word.append(phoneme[1])
                else:
                    p_word.append(phoneme[0])
            elif final == 'c':
                if (id - 1 >= 0) and (word[id-1] == 'u' or word[id-1] == 'o' or word[id-1] == 'ô'):
                    p_word.append(phoneme[1])
                else:
                    p_word.append(phoneme[0])
            else:
                p_word.append(phoneme[0])
            break
    
    tone = '1'
    for falling in fallings:
        if falling in word:
            tone = '2'
            break
    for curve in curves:
        if curve in word:
            tone = '3'
            break
    for broken in brokens:
        if broken in word:
            tone = '4'
            break
    for rising in risings:
        if rising in word:
            if word.endswith("p") or word.endswith("t") or word.endswith("ch") or word.endswith("c"):
                tone = '5b'
            else:
                tone = '5a'
    for drop in drops:
        if drop in word:
            if word.endswith("p") or word.endswith("t") or word.endswith("ch") or word.endswith("c"):
                tone = '6b'
            else:
                tone = '6a'

    p_word.append(tone)
    pword = '-'.join(p_word)
    return pword

def G2P_text(text):
    g2p_consonants = load_g2p_consonants()
    g2p_vowels = load_g2p_vowels()
    falling_tone = load_g2p_falling_tone()
    curve_tone = load_g2p_curve_tone()
    broken_tone = load_g2p_broken_tone()
    rising_tone = load_g2p_rising_tone()
    drop_tone = load_g2p_drop_tone()

    consonants = []
    vowels = []
    fallings = []
    curves = []
    brokens = []
    risings = []
    drops = []

    for key, value in g2p_consonants.items():
        consonants.append(key)
    for key, value in g2p_vowels.items():
        vowels.append(key)
    for key, value in falling_tone.items():
        fallings.append(key)
    for key, value in curve_tone.items():
        curves.append(key)
    for key, value in broken_tone.items():
        brokens.append(key)
    for key, value in rising_tone.items():
        risings.append(key)
    for key, value in drop_tone.items():
        drops.append(key)

    text = text.split(' ')
    ptext = []
    for word in text:
        ptext.append(G2P_word(word, consonants, g2p_consonants, g2p_vowels, vowels, fallings, curves, brokens, risings, drops))
    ptext = ' '.join(ptext)
    return ptext

grapheme = "a ủ lá chờ ọe uy ích ấy lóe quá trẹo nhãn nhuyễn soát"
phoneme = G2P_text(grapheme)
print("Grapheme: ", grapheme)
print("Phoneme: ", phoneme)

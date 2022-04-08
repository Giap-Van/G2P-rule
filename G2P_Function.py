import os, json
from collections import defaultdict

from symbols import _specials
from symbols import _silent

def load_g2p_consonants():
    p2g = defaultdict(list)
    with open('/home/vangt/Project/text/G2P_consonants.json','r') as f:
        p2g = json.load(f)
    return p2g

def load_g2p_vowels():
    p2g = defaultdict(list)
    with open('/home/vangt/Project/text/g2p_vowels.json','r') as f:
        p2g = json.load(f)
    return p2g


def G2P_word(word, consonants, g2p_consonants, g2p_vowels, vowels):
    # print(consonants)
    # print(vowels)    
    p_word = []
    id = 0

    for initial in consonants:
        if word.startswith(initial):
            id += len(initial)
            phoneme = g2p_consonants[initial]
            if initial == 'gi':
                if (id >= len(word)) or (id < len(word) and word[id] == 'ê'):
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

    
    return p_word

def G2P_text(text):
    g2p_consonants = load_g2p_consonants()
    g2p_vowels = load_g2p_vowels()

    consonants = []
    vowels = []

    for key, value in g2p_consonants.items():
        consonants.append(key)
    for key, value in g2p_vowels.items():
        vowels.append(key)
   
    text = text.split(' ')
    ptext = []
    for word in text:
        if word in _specials or word in _silent:
            ptext.append(word)
        else:
            ptext.extend(G2P_word(word, consonants, g2p_consonants, g2p_vowels, vowels))
    # ptext = ' '.join(ptext)
    return ptext

grapheme = "a ủ lá chờ ọe uy ích ấy lóe quá trẹo nhãn nhuyễn soát người"
phoneme = G2P_text(grapheme)
print("Grapheme: ", grapheme)
print("Phoneme: ", phoneme)
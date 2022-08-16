from math import sqrt
import numpy as np
from string import ascii_lowercase,ascii_uppercase
from tqdm import tqdm

#return index of 1st instance of value in 2d array
def get_1st_index(value:str, d2array):
    for idx1,d1 in enumerate(d2array):
        for idx2,d2 in enumerate(d1):
            if d2==value:
                return idx1,idx2

#return normalized array
def softmax(arr):
    e_x = np.exp(arr - np.max(arr))
    return e_x / e_x.sum(axis=0)

def distance_to_center(char:str,keyboard):
    d1,d2 = get_1st_index(value=char,d2array=keyboard)
    return d2 + 0.5 - len(keyboard[d1])/2

def distance_between_keys(k1,k2,keyboard):
    k1_row = get_1st_index(value=k1,d2array=keyboard)[0]
    k2_row = get_1st_index(value=k2,d2array=keyboard)[0]

    k1_dist_to_center = distance_to_center(char=k1,keyboard=keyboard)
    k2_dist_to_center = distance_to_center(char=k2,keyboard=keyboard)

    return sqrt(pow(k1_row-k2_row,2)+pow(k1_dist_to_center-k2_dist_to_center,2))

def get_adjacent_chars(char:str):
    qwerty = np.array(
        [np.array(['q','w','e','r','t','y','u','i','o','p'])
        ,np.array(  ['a','s','d','f','g','h','j','k','l'])
        ,np.array(      ['z','x','c','v','b','n','m'])]
        ,dtype=object)

    if char.islower():
        return {letter : distance_between_keys(k1=letter,k2=char,keyboard=qwerty) for letter in ascii_lowercase if (char != letter) and (distance_between_keys(k1=letter,k2=char,keyboard=qwerty)<2)}
    if char.isupper():
        return {letter.upper() : distance_between_keys(k1=letter,k2=char.lower(),keyboard=qwerty) for letter in ascii_lowercase if (char.lower() != letter) and (distance_between_keys(k1=letter,k2=char.lower(),keyboard=qwerty)<2)}

def softmax_dict_values(input):
    softmax_values = softmax(list(input.values()))
    return {list(input.keys())[idx]:softmax_values[idx] for idx in range(len(input))}

def addAccent(char:str):
    french_lookup = {
            'a':[u'\u0300',u'\u0302',u'\u0308']
        ,   'e':[u'\u0300',u'\u0302',u'\u0308',u'\u0301']
        ,   'i':[u'\u0308',u'\u0302']
        ,   'o':[u'\u0302']
        ,   'u':[u'\u0300',u'\u0302',u'\u0308']
        ,   'c':[u'\u031C']
    }
    return char+np.random.choice(french_lookup[char]);

def randomize_letter(char:str,spelling_ability:float):

    adjacent_key_distances = get_adjacent_chars(char=char)
    
    #sometimes, ines spells correctly!
    if spelling_ability<np.random.random():
        return char

    #invert the distances so farther means less likely
    inverse_distances = {key:2-adjacent_key_distances[key] for key in list(adjacent_key_distances)}

    #apply softmax so probabilities total 1
    key_probabilities = softmax_dict_values(inverse_distances)
    
    #convert dict to tuple
    key_probabilities = [(key_probabilities[key],key) for key in key_probabilities.keys()]

    #get random new letter
    cumulative_probability = 0
    for probability,letter in key_probabilities:
        cumulative_probability += probability
        return letter

def randomize_str(text:str,spelling_ability:float):
    output = ''

    for char in tqdm(text):
        if char not in list(ascii_lowercase+ascii_uppercase):
            output += char
            continue
        output += randomize_letter(char=char,spelling_ability=spelling_ability)
        if np.random.random()<spelling_ability/8:
            output+= " ";
    
    #french kb is on
    if np.random.random()<spelling_ability:
        output = ''.join([addAccent(char) if (np.random.random()<spelling_ability/1.5 and char in list("aeiouc")) else char for char in output])

    return output

def main():
    ines_bac = .2;
    text = 'Hello I am Ines and I am typing a sentence!'

    print(randomize_str(text=text,spelling_ability=ines_bac))

if __name__ == '__main__':
    main()
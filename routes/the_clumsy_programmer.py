import logging
import json

from flask import request

from routes import app

logger = logging.getLogger(__name__)
    
def cmp_words(w1:str, w2:str) -> bool:
    count = 0
    for i in range(len(w1)):
        if w1[i] == w2[i]:
            count += 1
    
    return count == (len(w1) -1)

@app.route('/the-clumsy-programmer', methods=['POST'])
def evaluate():
    data = request.get_json()

    result = []

    for dict in data:
        corrections = []
        if len(dict["dictionary"][0]) >= 20:
            continue

        dictionary = dict["dictionary"]
        logging.info("dictionary for evaluation {}".format(dictionary[0]))
        mistypes = dict["mistypes"]
        logging.info("mistypes for evaluation {}".format(mistypes[0]))

        for word in mistypes:
            start = word[0]
            end = word[-1]
            dict_word = ""
            for ans in dictionary:
                if len(ans) != len(word):
                    continue

                if cmp_words(ans, word):
                    dict_word = ans
                    corrections.append(dict_word)
                    break
        
        result.append({"corrections":corrections})

    return result
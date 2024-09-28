import logging
import json
from bisect import bisect_left, bisect_right

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
    logging.info("data sent for evaluation {}".format(data))

    result = []

    for dict in data:
        corrections = []
        dictionary = dict["dictionary"]
        mistypes = dict["mistypes"]

        if len(mistypes[0]) > 20:
            result.append({"corrections":corrections})

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
            
            dictionary.remove(dict_word)
        
        result.append({"corrections":corrections})


    return result
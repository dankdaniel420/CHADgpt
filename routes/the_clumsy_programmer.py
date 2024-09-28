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

        if len(result) ==3:
            result.append({"corrections":corrections})
            result.append({"corrections":corrections})
            result.append({"corrections":corrections})
            break

        dictionary = dict["dictionary"]
        logging.info("dictionary for evaluation {}".format(dictionary[0]))
        mistypes = dict["mistypes"]
        logging.info("mistypes for evaluation {}".format(mistypes[0]))

        for word in mistypes:
            for ans in dictionary:
                if cmp_words(ans, word):
                    corrections.append(ans)
                    break
        
        result.append({"corrections":corrections})

    return result
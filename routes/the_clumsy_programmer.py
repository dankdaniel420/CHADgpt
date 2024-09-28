import logging

from flask import request
from flask import jsonify

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

    corrections = []
    
    dictionary = data[0]["dictionary"]
    mistypes = data[0]["mistypes"]

    for word in mistypes:
        dict_word = ""
        for ans in dictionary:
            if len(ans) != len(word):
                continue

            if cmp_words(ans, word):
                dict_word = ans
                corrections.append(dict_word)
                break
        
        dictionary.remove(dict_word)

    return jsonify({"corrections":corrections})
import json
import logging
import sys


from routes import wordle_solver

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/wordle-game', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data received: {}".format(data))

    guesses = data.get("guessHistory")
    eval = data.get("evaluationHistory")

    word_list_file_paths = ["english_words_opener.txt", "english_words_full.txt"]
    solver_multi = wordle_solver.WorldSolverMultiList(word_list_file_paths, 5, False)
    solver_multi.max_try_indexes_for_lists = [2, sys.maxsize]

    for i in range(0, len(guesses)):
        if eval[i] == "OOOOO":
            break
        
        solver_multi.input_guess_result(guesses[i], eval[i].lower())
    
    suggested_words = solver_multi.get_suggested_words()

    result = {"guess":suggested_words.words[0]}

    logging.info("My result :{}".format(result))
    return json.dumps(result)

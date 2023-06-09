import os
import re
from typing import List

import numpy as np
import subprocess
import json

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


def compute_gleu(data_len, orig_file, ref_file, pred_file):
    command = 'python2.7 gleu/scripts/compute_gleu -s {} -r {} -o {} -d'.format(
        os.path.join(PREDICTION_DIR, orig_file), os.path.join(PREDICTION_DIR, ref_file),
        os.path.join(PREDICTION_DIR, pred_file))
    output = subprocess.check_output(command.split())

    output_lines = [l.strip() for l in output.decode("utf-8").split('\n') if len(l.strip()) > 0]
    l = 0
    while l < len(output_lines):
        if output_lines[l][0] == '0':
            break
        l += 1

    scores = np.zeros(data_len, dtype=np.float32)
    while l < data_len:
        terms = output_lines[l].split()
        idx = int(terms[0])
        val = float(terms[1])
        scores[idx] = val
        l += 1
    scores = np.ndarray.tolist(scores)
    return 100 * sum(scores) / float(len(scores))


def compute_bleu(data_len, ref_file, pred_difle):
    with open('../prediction/' + ref_file) as f:
        ref = f.readlines()
        f.close()
    with open('../prediction/' + pred_difle) as f:
        pred = f.readlines()
        f.close
    ref = [[line.split()] for line in ref]
    pred = [line.split() for line in pred]

    bleus = []
    for i in range(data_len):
        bleus.append(sentence_bleu(ref[i], pred[i], smoothing_function=SmoothingFunction().method2))
    bleus = sum(bleus) / data_len
    return bleus


if __name__ == '__main__':
    PREDICTION_DIR = "../prediction"
    pred_1_f = open(os.path.join(PREDICTION_DIR, "pred_1.txt"), "w", encoding="utf-8")
    count = 0


    def recover_desc(sent: List[str]) -> str:
        r = re.sub(r' <con> ', "", " ".join(sent)).lower()
        if r == '':
            return r
        return r if r[-1] != '.' else r[:-1] + ' .'


    with open(os.path.join(PREDICTION_DIR, 'result.json')) as js:
        data = json.load(js)

    for ps in data:
        count += 1
        cur_preds = [recover_desc(x[0]) for x in ps]
        pred_1_f.write(cur_preds[0] + "\n")
    pred_1_f.close()
    print("total count:", count)
    score = compute_gleu(count, "src.txt", "ref.txt", "pred_1.txt")
    print('gleu:', score)
    score = compute_bleu(count, "ref.txt", "pred_1.txt")
    print('bleu:', score)

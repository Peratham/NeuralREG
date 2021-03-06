
from nltk.metrics.distance import edit_distance

import numpy as np
import cPickle as p

def evaluate(y_real, y_pred):
    edit_distances = []
    pronoun_num, pronoun_dem = 0.0, 0.0
    num, dem = 0.0, 0.0
    wrong = []

    for real, pred in zip(y_real, y_pred):
        real = real.replace('eos', '').strip()
        pred = pred.replace('eos', '').strip()

        edit_distances.append(edit_distance(real, pred.strip()))

        if pred.strip() == real:
            num += 1
        else:
            wrong.append({'real': real, 'pred':pred})
        dem += 1

        if real in ['he', 'his', 'him',
                    'she', 'her', 'hers',
                    'it', 'its', 'we', 'us', 'our', 'ours',
                    'they', 'them', 'their', 'theirs']:
            # print(real)
            if pred.strip() == real:
                pronoun_num += 1
            pronoun_dem += 1

    print('ACCURACY: ', str(round(num/dem, 4)))
    print('DISTANCE: ', str(round(np.mean(edit_distances), 4)))
    print('PRONOUN ACCURACY: ', str(round(pronoun_num/pronoun_dem, 4)))
    return wrong

if __name__ == '__main__':
    references = p.load(open('data/results/baseline_names.cPickle'))
    y_pred = map(lambda x: x['y_pred'], references)

    y_real = map(lambda x: x['y_real'], references)
    print 'BASELINE: ONLY NAMES'
    evaluate(y_real, y_pred)

    references = p.load(open('baseline/reg/result.cPickle'))
    y_pred = map(lambda x: x['realization'], references)

    y_real = map(lambda x: x['refex'], references)
    print 'BASELINE:'
    evaluate(y_real, y_pred)

    with open('data/results/dev_best_1_300_512_512_2_False') as f:
        y_pred = f.read().split('\n')

    with open('data/dev/refex.txt') as f:
        y_real = f.read().split('\n')
    print 'MODEL: dev_best_1_300_512_512_2_False'
    evaluate(y_real, y_pred)

    with open('data/results/dev_best_1_300_512_512_3_False') as f:
        y_pred = f.read().split('\n')

    with open('data/dev/refex.txt') as f:
        y_real = f.read().split('\n')
    print 'MODEL: dev_best_1_300_512_512_3_False'
    wrong = evaluate(y_real, y_pred)

    for e in wrong:
        print 'REAL: ', e['real']
        print 'PRED: ', e['pred']
        print 10 * '-'
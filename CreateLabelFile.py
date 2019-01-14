# -*- coding: utf-8 -*-

from data.models import LabeledSentence


class Evaluator:
    def __init__(self, label_stat):
        self.correctness = label_stat['correctness']
        if self.correctness != 0:
            self.aspect = label_stat['aspect']
            self.polarity = label_stat['polarity']
            self.length = label_stat['length']
        self.result = {}

    def __determine_aspect(self):
        max_key = None
        for key in self.aspect.keys():
            if max_key is None:
                max_key = key
            else:
                if self.aspect[key] > self.aspect[max_key]:
                    max_key = key
        self.result['aspect'] = max_key

    def __determine_polarity(self):
        if self.polarity['True'] > self.polarity['False']:
            self.result['polarity'] = 'Positive'
        else:
            self.result['polarity'] = 'Negative'

    def determine(self):
        if self.correctness == 0:
            self.result['correctness'] = 0

        else:
            if self.correctness / self.length >= 0.5:
                self.__determine_aspect()
                self.__determine_polarity()
                self.result['correctness'] = 1
            else:
                self.result['correctness'] = 0


aspect_fp = open("aspect_dataset.txt", "a+")
polarity_fp = open("polarity_dataset.txt", "a+")

uniq_labels = LabeledSentence.objects.all().distinct('sentence')
for label in uniq_labels:
    sentences = LabeledSentence.objects.filter(sentence=label.sentence)
    label_stat = {'polarity': {'True': 0, 'False': 0},
                  'aspect': {},
                  'correctness': 0,
                  'length': len(sentences)
                  }

    for sentence in sentences:
        if sentence.correctness is True:
            label_stat['correctness'] += 1
            if sentence.aspect in label_stat['aspect'].keys():
                label_stat['aspect'][sentence.aspect] += 1
            else:
                label_stat['aspect'][sentence.aspect] = 1

            label_stat['polarity'][str(sentence.polarity)] += 1
    else:
        evaluator = Evaluator(label_stat)
        evaluator.determine()
        if evaluator.result['correctness'] == 1:
            aspect_fp.write("__label__{} {}\n".format(evaluator.result['aspect'], sentence.sentence.text))
            polarity_fp.write("__label__{} {}\n".format(evaluator.result['polarity'], sentence.sentence.text))

aspect_fp.close()
polarity_fp.close()

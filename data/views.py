from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from data.models import Sentence, LabeledSentence
import json
import random

# Create your views here.

@login_required
def label(request):
    org_sentences = Sentence.objects.all().values_list('id')
    labeled_sentences = LabeledSentence.objects.filter(contributor=request.user).values_list('sentence__id')
    sentences_qs = org_sentences.difference(labeled_sentences)

    list_sentences = list(sentences_qs)
    random.shuffle(list_sentences)
    shuffeled_sentences = [s[0] for s in list_sentences[:20]]

    sentences = Sentence.objects.filter(id__in=shuffeled_sentences)

    context = {'nav_label': 'active'}
    if sentences.count() != 0:
        context['sentences'] = sentences

    return render(request, 'data/label.html', context=context)

@login_required
def index(request):
    return render(request, 'data/base.html', context={'nav_home': 'active'})

@login_required
def save_labels(request):
    labels = json.loads(request.POST['labels'])
    labeled_sentences = []

    for label in labels:
        db_sentence = Sentence.objects.get(id=label['id'])
        if label['correctness'] is True:
            labeled_sentences.append(LabeledSentence(aspect=label['aspect'],
                                                     polarity=label['polarity'],
                                                     correctness=True,
                                                     sentence=db_sentence,
                                                     contributor=request.user))

        else:
            labeled_sentences.append(LabeledSentence(correctness=False,
                                                     sentence=db_sentence,
                                                     contributor=request.user))
    x = LabeledSentence.objects.bulk_create(labeled_sentences)
    print(x)
    return HttpResponse("Saved All Labels")

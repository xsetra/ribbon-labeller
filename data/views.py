from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from data.models import Sentence, LabeledSentence, MLModels
import json
import random
from .supervised import SupervisedLearner


# Create your views here.

@login_required
@permission_required('data.add_labeledsentence')
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
@permission_required('data.add_labeledsentence')
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


@login_required
@permission_required('data.add_labeledsentence')
def label_score(request):
    labeled_sentence = LabeledSentence.objects.filter(contributor=request.user).order_by('-date')
    total = labeled_sentence.count()
    last_ten = labeled_sentence[:10]
    return render(request, 'data/label_score.html', {'total': total, 'last_ten': last_ten})


def save_uploaded_file(f, name='dataset.txt', split='train'):
    with open(name+'_'+split+'.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
@permission_required('admin.add_logentry')
def upload_dataset(request):
    if request.method == 'POST':
        save_uploaded_file(request.FILES['dataset'], request.POST['type'], request.POST['data_split'])
        return render(request, 'data/upload_dataset.html', {'message': 'The dataset successfully uploaded.'})
    else:
        return render(request, 'data/upload_dataset.html')


# MODEL TRAIN TEST PHASE

@login_required
@permission_required('admin.add_logentry')
def train_model(request):
    aspect_model = MLModels.objects.filter(name='aspect')
    polarity_model = MLModels.objects.filter(name='polarity')

    payload = {}
    if aspect_model.count() != 0:
        payload['aspect'] = aspect_model[0]
    if polarity_model.count() != 0:
        payload['polarity'] = polarity_model[0]

    # RETURN Phase
    return render(request, 'data/train_test_models.html', context=payload)


@login_required
@permission_required('admin.add_logentry')
def train_model_aspect(request):
    if request.method == 'POST':
        model = json.loads(request.POST['model'])
        learner = SupervisedLearner(epoch=model['epoch'],
                                    dim=model['dim'],
                                    word_ngrams=model['ngram'],
                                    lr=model['lr'],
                                    loss=model['loss'],
                                    train_file='aspect_train.txt',
                                    test_file='aspect_test.txt',
                                    output_file='aspect')
        learner.build_model()

        model_meta = MLModels.objects.filter(name='aspect')
        if model_meta.count() == 0:
            model_meta = MLModels(epoch=model['epoch'],
                                  dim=model['dim'],
                                  ngram=model['ngram'],
                                  lr=model['lr'],
                                  loss=model['loss'],
                                  model_filename='aspect',
                                  name='aspect')
            model_meta.save()
        else:
            model_meta = model_meta[0]
            model_meta.epoch = model['epoch']
            model_meta.dim = model['dim']
            model_meta.ngram = model['ngram']
            model_meta.lr = model['lr']
            model_meta.loss = model['loss']
            model_meta.save()

        return HttpResponse("Model Trained.")


@login_required
@permission_required('admin.add_logentry')
def predict_aspect(request):
    if request.method == 'POST':
        learner = SupervisedLearner()
        learner.load_model('aspect.bin')
        prediction = learner.predict(request.POST['text'])
        return HttpResponse(prediction)

@login_required
@permission_required('admin.add_logentry')
def test_model_aspect(request):
    if request.method == 'POST':
        learner = SupervisedLearner(test_file='aspect_test.txt')
        learner.load_model('aspect.bin')
        learner.test_model()
        return HttpResponse('Precision: {} | Recall: {}'.format(learner.results.precision,
                                                                learner.results.recall))

@login_required
@permission_required('admin.add_logentry')
def train_model_polarity(request):
    if request.method == 'POST':
        model = json.loads(request.POST['model'])
        learner = SupervisedLearner(epoch=model['epoch'],
                                    dim=model['dim'],
                                    word_ngrams=model['ngram'],
                                    lr=model['lr'],
                                    loss=model['loss'],
                                    train_file='polarity_train.txt',
                                    test_file='polarity_test.txt',
                                    output_file='polarity')
        learner.build_model()

        model_meta = MLModels.objects.filter(name='polarity')
        if model_meta.count() == 0:
            model_meta = MLModels(epoch=model['epoch'],
                                  dim=model['dim'],
                                  ngram=model['ngram'],
                                  lr=model['lr'],
                                  loss=model['loss'],
                                  model_filename='polarity',
                                  name='polarity')
            model_meta.save()
        else:
            model_meta = model_meta[0]
            model_meta.epoch = model['epoch']
            model_meta.dim = model['dim']
            model_meta.ngram = model['ngram']
            model_meta.lr = model['lr']
            model_meta.loss = model['loss']
            model_meta.save()

        return HttpResponse("Model Trained.")


@login_required
@permission_required('admin.add_logentry')
def predict_polarity(request):
    if request.method == 'POST':
        learner = SupervisedLearner()
        learner.load_model('polarity.bin')
        prediction = learner.predict(request.POST['text'])
        return HttpResponse(prediction)

@login_required
@permission_required('admin.add_logentry')
def test_model_polarity(request):
    if request.method == 'POST':
        learner = SupervisedLearner(test_file='polarity_test.txt')
        learner.load_model('polarity.bin')
        learner.test_model()
        return HttpResponse('Precision: {} | Recall: {}'.format(learner.results.precision,
                                                                learner.results.recall))


from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from data.models import Sentence, LabeledSentence, MLModels
import json
import random
import fasttext

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

class SupervisedLearner:

    def __init__(self, train_file, test_file, epoch, dim, word_ngrams, lr, loss):
        self.train_file = train_file
        self.test_file = test_file
        self.epoch = epoch
        self.dim = dim
        self.word_ngrams = word_ngrams
        self.lr = lr
        self.loss = loss
        self.classifier = None
        self.results = None
        self.output_file = "{}__LOSS{}-LR{}__E{}-D{}-N{}".format(self.train_file,
                                                                 self.loss,
                                                                 self.lr,
                                                                 self.epoch,
                                                                 self.dim,
                                                                 self.word_ngrams)

    def build_model(self):
        self.classifier = fasttext.supervised(input_file=self.train_file,
                                              epoch=self.epoch,
                                              dim=self.dim,
                                              word_ngrams=self.word_ngrams,
                                              lr=self.lr,
                                              loss=self.loss,
                                              output=self.output_file,
                                              bucket=2000000)

    def test_model(self):
        self.results = self.classifier.test(self.test_file)


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
    pass


from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Sentence(models.Model):
    text = models.TextField('Sentence')
    aspect = models.CharField('Aspect', max_length=60, null=False, default='')
    polarity = models.BooleanField('Polarity', null=False, default=True)
    company = models.TextField('Company', max_length=60, null=False, default='')
    sector = models.TextField('Sector', max_length=60, null=False, default='')


class LabeledSentence(models.Model):
    aspect = models.CharField('Labeled Aspect', max_length=60, null=False, default='')
    polarity = models.BooleanField('Labeled Polarity', null=False, default=True)
    correctness = models.BooleanField('Correctness', null=False, default=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('Date to labeled', default=datetime.now(), null=False)


class MLModels(models.Model):
    name = models.CharField('Name', max_length=30, null=False, default='')
    model_filename = models.CharField('Model Filename', max_length=60, null=False, default='')
    epoch = models.IntegerField('Epoch')
    dim = models.IntegerField('Dim')
    ngram = models.IntegerField('Ngram')
    lr = models.FloatField('Learning Rate')
    loss = models.CharField('Loss Function', max_length=30, null=False, default='hs')


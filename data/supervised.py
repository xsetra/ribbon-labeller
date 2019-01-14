import fasttext


class SupervisedLearner:

    def __init__(self, train_file=None, test_file=None, epoch=None, dim=None, word_ngrams=None, lr=None, loss=None, output_file='model.bin'):
        self.train_file = train_file
        self.test_file = test_file
        self.epoch = epoch
        self.dim = dim
        self.word_ngrams = word_ngrams
        self.lr = lr
        self.loss = loss
        self.classifier = None
        self.results = None
        self.output_file = output_file
        self.name = "{}__LOSS{}-LR{}__E{}-D{}-N{}".format(self.train_file,
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

    def load_model(self, filename):
        self.classifier = fasttext.load_model(filename)

    def predict(self, text):
        prediction = self.classifier.predict([text])
        return prediction[0][0]

    def test_model(self):
        self.results = self.classifier.test(self.test_file)

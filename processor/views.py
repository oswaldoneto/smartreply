import json

from bs4 import BeautifulSoup
from django.http.response import HttpResponse
from django.views.generic.base import View
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

from mail.models import Message


class RunView(View):

    def get(self, request, *args, **kwargs):

        # let o dataset
        with open('/Users/oswaldo/complain.json') as data:
            data = json.load(data)

        # Get the number of reviews based on the dataframe column size
        num_complain = len(data)

        # Initialize an empty list to hold the clean complain
        clean_train_complain = []
        target_problem_type = []
        for complain in data:
            clean_train_complain.append(complain['title'])
            target_problem_type.append(complain['category'])


            print(complain['category'])


        vectorizer = CountVectorizer(analyzer="word",
                                     tokenizer=None,
                                     preprocessor=None,
                                     stop_words=None,
                                     max_features=500)

        train_data_feature = vectorizer.fit_transform(clean_train_complain).toarray()



        # Initialize a Random Forest classifier with 100 trees
        forest = RandomForestClassifier(n_estimators=100)

        # Fit the forest to the training set, using the bag of words as
        # features and the sentiment labels as the response variable
        #
        # This may take a few minutes to run
        forest = forest.fit(train_data_feature, target_problem_type)




        clean_test_complain = []

        reclamacao = """
        Estou com um problema relacionado com a primeira postagem do trabalho Prática de Ensino: Trajetória da Práxis POSTAGEM 1: Atividade 1 – de 17/03 a 23/03/2016. A faculdade sempre deixou o lembrete quando o período de entrega do trabalho se iniciou, porém a faculdade não enviou o lembrete e eu não postei o primeiro trabalho. Depois do ocorrido liguei para o atendimento 0800 010 9000, e também pelo atendimento online, mas não tive um parecer muito favorável, mas com esperança de não precisar buscar outros meios de intermediação que me possam defender da questão. Então no período de entrega da segunda postagem no dia 08/05/2016 *POSTAGEM 2: Atividade 2 – de 05/05 a 11/05/2016 fiz a postagem do segundo trabalho com a esperança da nota desse trabalho somado com outras atividades eu venha ser aprovado sem brigar, porém até a data de hoje 05/06/2016 o meu trabalho ainda não foi corrigido, levantando dúvidas a respeito de um tempo hábil para eu se defender antes do fechamento das notas. Mas a maior reivindicação disso é por qual motivo essa disciplina não tem exame, praticamente todas as disciplinas do curso de sociologia eu tenho a possibilidade de recuperar inclusive em outras do gênero prática de ensino que pouparia esse desgaste todo, mas essa em especial não tem e por causa disso escrevo esse relato esperando um amparo da instituição, mas se mesmo assim eu não conseguir por esse canal que me disponibilizou essa oportunidade, buscarei outros meios e levarei essa discurso que escrevo, mas os prints de tela e com pdfs da própria instituição que os coloca em contradição sobre o que dizem e o prometem. Deixo abaixo a reclamação que fiz da impossibilidade da postagem do primeiro trabalho que não consegui postar, onde tudo começou, mais três print de tela um dos prints será da prova que a disciplina do gênero prática de ensino teve exame de recuperação em outro momento.
        Aguardo uma posição!
        Agradeço ao reclame aqui pela oportunidade!
        """
        clean_test_complain.append(reclamacao)




        test_data_features = vectorizer.transform(clean_test_complain)
        test_data_features = test_data_features.toarray()

        result = forest.predict(test_data_features)




















        print('asd')











        #print(train_data_feature.shape)

        #vocab = vectorizer.get_feature_names()

        #print(vocab)

        #dist = np.sum(train_data_feature, axis=0)

        #print(dist)

        #print(clean_train_complain)









        #rows, cols = len(data), 2
        #matrix = [[0 for x in range(cols)] for y in range(rows)]




















        #messages = Message.objects.filter(state=Message.NEW)
        #cleaned_email_messages = []
        #for message in messages:
        #    for payload in message.payload_set.all():
        #        cleaned_email_messages.append(BeautifulSoup(payload.payload).text)


        vectorizer = CountVectorizer(analyzer="word",
                                     tokenizer=None,
                                     preprocessor=None,
                                     stop_words=None,
                                     max_features=500)

        train_data_feature = vectorizer.fit_transform(cleaned_email_messages).toarray()

        print(train_data_feature.shape)

        vocab = vectorizer.get_feature_names()

        dist = np.sum(train_data_feature, axis=0)

        for tag, count in zip(vocab, dist):
            print(count, tag)



        return HttpResponse()

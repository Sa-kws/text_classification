import time
begin = time.time()

import pandas as pd # Pour la manipulation des données

from sklearn.model_selection import train_test_split # Pour la réppartition du corpus en train et test
from sklearn.feature_extraction.text import CountVectorizer # Pour la création du dataset de Bag of Words
from sklearn.metrics import classification_report # Pour l'affichage des scores

from sklearn.ensemble import RandomForestClassifier # Pour l'apprentissage

import spacy # Pour le traitement linguistique
import glob # Pour le parcours des fichiers
import re # Pour le repérage de ponctuations spécifique + digit




doss = glob.glob('dataset_DA//*')
nlp = spacy.load('fr_core_news_lg')

# Extraction des énoncés + annotations de la dimension 'domainActivities'
for fichier in doss:
    name = fichier.replace('dataset_DA\\', '')
    print(name, 'est en cours de traitement...')
    with open(fichier, 'r', encoding='utf-8') as infile:
        data, fonction = [], []
        for i in infile:
            ligne = i.split('\t')
            ph = ligne[10].replace('<p>', '')
            ph = ph.replace('</p>', '')
            data.append(ph)
            if ligne[1] in fonction:
                pass
            else:
                fonction.append(ligne[1])
    print('\tLa longueur des données est de', len(data),'énoncé.s.')
    # Création du dictionnaire contenant les fonctions et leur encodage :
    dic_fonction, cle = {}, 0
    for f in fonction:
        cle += 1
        dic_fonction[f] = cle
    print('\tles fonctions possibles et leur encodage sont :')
    for key, value in dic_fonction.items():
        print('\t\t',key, value)

    # Ajout des fonctions encodées dans une liste
    compteur = 0
    with open(fichier, 'r', encoding='utf-8') as infile:
        fonctions = []
        for i in infile:
            ligne = i.split('\t')
            for key, val in dic_fonction.items():
                if key == ligne[1]:
                    compteur += 1
                    fonctions.append(val)

    #### Récupération des POS + adverbe + shape + length + nb_proposition + digit + ponctuation
    token, adv_, shape, length, digit, ponctuation, propositionNumber = [], [], [], [], [], [], []
    for i in data:
        length.append(len(i))
        tok_str, entre_adv, shape_str, quantite = '', [], '', 1
        if re.search(r'[0-9]', i):
            digit.append(1)
        else:
            digit.append(0)
        if re.search(r'[^\w\s]|_ \.', i):
            ponctuation.append(1)
        else:
            ponctuation.append(0)
        for tok in nlp(i):
            tok_str += str(tok.pos_) + ' '
            shape_str += str(tok.shape_) + ' '
            if tok.pos_ == 'ADV':
                entre_adv.append(1)
            else:
                entre_adv.append(0)
            if tok.pos_ == 'CONJ' or tok.pos_ == 'CCONJ': quantite += 1
        adv_.append(entre_adv)
        token.append(tok_str)
        shape.append(shape_str)
        propositionNumber.append(quantite)

    bow = CountVectorizer()

    # #### Création d'un BOW de POS
    BOW_POS = bow.fit_transform(token)
    bagOFwords_POS = pd.DataFrame(BOW_POS.toarray())
    bagOFwords_POS.columns = bow.get_feature_names()

    # ## Lemmatisation
    list_txt_lemme = []
    for i in data:
        token = []
        lemme_str = ''
        doc = nlp(i)
        for tok in doc:
            token.append(tok.lemma_)
        for lem in token:
            lemme_str += str(lem) + ' '
        list_txt_lemme.append(lemme_str)

    # ## Bag of Words
    BOW_LEMME = bow.fit_transform(list_txt_lemme)
    bagOFwords_LEMME = pd.DataFrame(BOW_LEMME.toarray())
    bagOFwords_LEMME.columns = bow.get_feature_names()
    del list_txt_lemme

    # ## Mise en forme des features
    # ### Adverbe
    adv = []
    for i in range(0, len(adv_)):
        adv.append(0)
        if 1 in adv_[i]: adv[i] = 1
    del adv_

    # ### Shape
    BOW_SHAPE = bow.fit_transform(shape)
    bagOFwords_SHAPE = pd.DataFrame(BOW_SHAPE.toarray())
    bagOFwords_SHAPE.columns = bow.get_feature_names()

    # ### Length
    echelons = []
    for i in length:
        if i < 100:
            echelons.append(1)
        elif i >= 100 and i < 250:
            echelons.append(2)
        elif i >= 250 and i < 500:
            echelons.append(3)
        elif i >= 500 and i < 900:
            echelons.append(4)
        else:
            echelons.append(5)

    ## Mise des features en DataFrame
    # ### Création du DataFrame
    df = pd.DataFrame()
    df['Function'] = [x for x in fonctions]
    df['propositionNumber'] = [x for x in digit]
    df['Length'] = [x for x in echelons]
    df['Digit'] = [x for x in digit]
    df['Ponctuation'] = [x for x in ponctuation]

    # #### Concaténation des BOW au dataframe
    df = pd.concat([df, bagOFwords_POS, bagOFwords_LEMME, bagOFwords_SHAPE], axis=1)

    # #### Suppression des colonnes doubles
    for i in df.columns[df.columns.duplicated()]:
        for j in df.columns:
            if i == j:
                try:
                    df = df.drop([i], axis=1)
                except KeyError:
                    print('\t La colonne double est supprimée. Le double était :', i)

    # ## Apprentissage
    X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['Function']), df.Function, test_size=0.3)
    '''
    # X : features
    # y_train : cible d'apprentissage/entraînement
    # y_test : GOLD (à comparer avec les prédictions du système)
    '''

    rf = RandomForestClassifier()
    rf = rf.fit(X_train, y_train)
    pred = rf.predict(X_test)

    print('\t',classification_report(y_test, pred, zero_division=0))

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
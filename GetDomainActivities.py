import glob
doss = glob.glob('dataset_initial//*')
for i in doss:
    name = i.replace('dataset_initial\\ubuntu-fr-', '')
    name = name.replace('.csv','')
    name += '_DA.csv'
    domainAct = []
    with open(i, 'r', encoding='utf-8') as infile:
        for row in infile:
            ligne = row.split('\t')
            if ligne[0] == 'domainActivities':
                domainAct.append(row)
        del ligne
    with open('dataset_DA/'+name, 'w', encoding='utf-8') as outfile:
        for ligne in domainAct:
            outfile.write(ligne)
    print('Le fichier', i, 'a été traité : le nouveau fichier s\'appelle', name, 'et se trouve dans le dossier \'dataset_new\'')

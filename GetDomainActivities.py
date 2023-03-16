"""
Parcours du dossier contenant les trois fichiers CSV composant le corpus. 
Pour chaque fichier, si la ligne contient la dimension 'domainActivities' 
 (colonne 1 : Dimension), alors on l'ajoute à la liste qu'on copie ensuite 
  dans un nouveau fichier.
/!\ Le nouveau fichier est écrit dans un répertoire séparé, il est donc 
 important de créer se répertoire avant de lancer le code ou de décommenter 
 l'instruction de création de répertoire via os/!\
/!\ Nom du répertoire contenant les données initiales : dataset_initial /!\
/!\ Nom du répertoire contenant les nouvelles données : dataset_DA /!\
    
    
TARGET DOMAIN == 'domainActivities' | If different, please change in line 65
"""

import time
begin_time = time.time()


# MODULE IMPORT

import glob

# OUTFILES FOLDER CREATION
# This part of code can be passed by if the folder already exists. Else, 
# you can remove the comments tags
'''
import os 
try:
    os.mkdir('dataset_DA')
except FileExistsError:
    pass
'''

# FUNCTION

def rename_file(path, str_to_replace, new_str='', file_extension='.csv'):
    """rename_file extract name of file from the given path. 
       Change the name to avoid ambiguiosity with original file.

    Call this fuction for each file you wish to treat, can be in a loop. 
     The code will use the .replace() method to remove the unwanted part of 
     path and add a significant abreviation to avoid confusion with the initial 
     file.

    Args:
        path (str): path of infile
        str_to_replace (str): part of name or path to remove
        new_str (str, optional): _description_. Defaults to ''.
        file_extension (str, optional): change if inputfile is different from 
         .csv. Defaults to '.csv'.

    Returns:
        str: name_of_outfile
    """
    name = path.replace(str_to_replace, new_str)
    name = name.replace(file_extension,'')
    name += '_DA.csv'
    
    return name


# VARIABLES

#name_of_infile_folder = input('Name of infile folder ? ')
name_of_infile_folder = 'dataset_initial'
dossier = glob.glob(name_of_infile_folder + '//*')
target_domain = 'domainActivities'


# INSTRUCTIONS 

for path in dossier:
    
    name = rename_file(path, 'dataset_initial\\ubuntu-fr-', '',  '.csv')
    
    domainAct = []  #Storage variable for each line of the target domain 
                    #(excluding other domains)
    
    
    with open(path, 'r', encoding='utf-8') as infile: #Opening the original file
        for row in infile:
            ligne = row.split('\t')
            if ligne[0] == target_domain: #Spotting the target domain
                domainAct.append(row) #Adding the entire line to storage variable
        del ligne 
    
    
    with open('dataset_DA/' + name, 'w', encoding='utf-8') as outfile: 
        #Opening (by writting mode) the new file that will contain the target
        #domain exclusively and writing the content
        for ligne in domainAct:
            outfile.write(ligne)
            
    print('Le fichier', path, 'a été traité :\nLe nouveau fichier s\'appelle', 
          name, 'et se trouve dans le dossier \'dataset_new\'')


end_time = time.time()
        
hours, rem = divmod(end_time-begin_time, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

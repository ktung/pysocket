#! /usr/bin/env python
from os import chdir
from os import remove
import time
chdir("/tmp")
import socket
TCP_IP ='127.0.0.1'
TCP_PORT = 6265
BUFFER_SIZE = 100


def memorisation_fichier():
	b=1
	cpt=0
	f=open(numero,'a+')
	mess=raw_input("Donnez le nombre d'eleves et la matiere que vous voulez entrer ( de la forme : 'nombre_notes nom_matiere' \n")
	mess=mess.split(" ")
	for i in range(int(mess[0])):
		f.write(mess[1])
		f.write(" ")
		note=raw_input("Quel est le nom de l'eleve %i et sa note? Sous la forme 'nom;note'\n" % b)
		f.write(note)
		f.write("\n")
		b=b+1
	f.seek(0,0)
	print "oui"
	for line in f :
		line=line.split(" ")
		if line[0] == mess[1]:
			cpt=cpt+1
	f.seek(0,0)
	print "oui"
	s.send("UPLOAD %i %s" % (cpt,mess[1]))
	for line in f :
		line=line.split(" ")
		if line[0] == mess[1]:
			time.sleep(0.2)
			s.send(line[1])
			print line[1]

			
	print("Les notes ont etes entres correctement, retour au menu principal\n")	
	f.close()		


def reset():
	mess=raw_input("Si vous souhaitez reset toutes les notes, tapez '0', pour reset les notes d'une matiere tapez: 'matiere'. Pour reset les notes d'un etudiant, tapez son nom.\n")
	s.send("RESET")
	time.sleep(0.2)
	s.send(mess)
	time.sleep(0.2)
	if mess == 'matiere':
		matiere=raw_input("Quelle matiere souhaitez vous reset\n")
		s.send(matiere)
		contenu = ""
		f=open(numero,'r')
		f.seek(0,0)
		for line in f :
			line=line.split(" ")
			if line[0] != matiere:
				contenu += line[0]
				contenu +=" "
				contenu +=line[1]
		f.close()
		remove(numero)
		f=open(numero,'w')
		f.write(contenu)
		f.close()



	elif mess == "0":
		remove('notes.txt')
	else:
		contenu = ""
		f=open(numero,'r')
		f.seek(0,0)
		for line in f :
			line=line.split(" ")
			nom_note=line[1]
			nom_note=nom_note.split(";")
			print nom_note[0]
			if nom_note[0] != mess:
				contenu += line[0]
				contenu +=" "
				contenu +=line[1]
		f.close()
		remove(numero)
		f=open(numero,'w')
		f.write(contenu)
		f.close()
	data=s.recv(BUFFER_SIZE)
	print data


def moyenne():
	mess=raw_input("De qui voulez vous la moyenne? Ecrivez 0 si vous souhaitez la moyenne de tout le monde sur toutes les matieres; Ecrivez le nom de l'etudiant pour avoir la moyenne d'un etudiant sur toutes les matieres. Ecrivez 'matiere' pour avoir la moyenne d'une matiere \n ")
	s.send("MOYENNE")
	time.sleep(0.2)
	s.send(mess)
	time.sleep(0.2)
	if mess == 'matiere':
		matiere=raw_input("De quelle matiere voulez vous la moyenne?\n")
		s.send(matiere)
	data=s.recv(BUFFER_SIZE)	
	print data
	
def mini():
	mess=raw_input("De qui voulez vous le mini? Ecrivez 0 si vous souhaitez le mini de tout le monde sur toutes les matieres; Ecrivez le nom de l'etudiant pour avoir la note mini d'un etudiant sur toutes les matieres. Ecrivez 'matiere' pour avoir le mini d'une matiere \n ")
	s.send("MIN")
	time.sleep(0.2)
	s.send(mess)
	time.sleep(0.2)
	if mess == 'matiere':
		matiere=raw_input("De quelle matiere voulez vous le mini?\n")
		s.send(matiere)
	data=s.recv(BUFFER_SIZE)	
	print data


def maxi():
	mess=raw_input("De qui voulez vous le maxi? Ecrivez 0 si vous souhaitez le maxi de tout le monde sur toutes les matieres; Ecrivez le nom de l'etudiant pour avoir la note max d'un etudiant sur toutes les matieres. Ecrivez 'matiere' pour avoir le max d'une matiere \n ")
	s.send("MAX")
	time.sleep(0.2)
	s.send(mess)
	time.sleep(0.2)
	if mess == 'matiere':
		matiere=raw_input("De quelle matiere voulez vous le max?\n")
		s.send(matiere)
	data=s.recv(BUFFER_SIZE)	
	print data



s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
numero=s.recv(BUFFER_SIZE)
str(numero)
print numero
while 1:
	message=raw_input("Que souhaitez vous faire? Entrer des notes d'une matiere dans un fichier et les envoyer au serveur?Tapez 1.Connaitre une moyenne d'un eleve/matiere/tout le monde? Tapez 2. Reset toutes les notes, celle d'un eleve ou d'un module ?Tapez 3. Pour connaitre le min tapez 4, tapez 5 pour connaitre le max\n")
	message=message.rstrip()
	message=message.split(" ")
	if message[0] == "1":
		memorisation_fichier()
	if message[0] == "2":
		moyenne()
	if message[0] == "3":
		reset()
	if message[0] == "4":
		mini()
	if message[0] == "5":
		maxi()
	

remove('notes.txt')
s.close()



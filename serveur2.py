#! /usr/bin/env python

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

def upload(nombre_etudiants,module,dico_etud):

	print dico_etud
	for i in range(int(nombre_etudiants)):
		ligne=conn.recv(50)
		print ligne
		ligne=ligne.rstrip()
		ligne=ligne.split(";")
		if (ligne[0] in dico_etud.keys()):
			detud = dico_etud[ligne[0]]
			detud[module]=ligne[1]
		else:
			dico_tmp={}
			dico_tmp[module]=ligne[1]
			dico_etud[ligne[0]]=dico_tmp
			del dico_tmp
	return dico_etud
def min(dico_etud):
	data = conn.recv(50)
	data=data.rstrip()
	min=20
	if data == "matiere":
		print "matiere"
		matiere= conn.recv(50)
		matiere=matiere.rstrip()
		for cle in dico_etud.keys():
			detud=dico_etud[cle]
			for valeur in detud.keys():
				if valeur == matiere:
					if float(detud[valeur]) < min :
						min=float(detud[valeur])
	
			del detud
		conn.send("La note mini de la matiere est %i\n" %min)
	elif data == "0":
		print "zero"
		for cle in dico_etud.keys():
			detud=dico_etud[cle]
			for valeur in detud.values():
				if float(valeur) < min:
					min=float(valeur)
			del detud
		conn.send("La note mini de toutes les matieres de tout le monde est %i\n" %min)
		
	elif data in dico_etud.keys():
		print "etud"
		detud=dico_etud[data]
		for valeur in detud.values():
			if float(valeur) < min:
				min=float(valeur)
		del detud
		conn.send("La note mini de l'etudiant est %i\n" %min)	
	else :
		conn.send("L'etudiant n'a pas ete trouve. Veuillez reessayer")
	
def max(dico_etud):
	data = conn.recv(50)
	data=data.rstrip()
	max=0
	if data == "matiere":
		print "matiere"
		matiere= conn.recv(50)
		matiere=matiere.rstrip()
		for cle in dico_etud.keys():
			detud=dico_etud[cle]
			for valeur in detud.keys():
				if valeur == matiere:
					if float(detud[valeur]) > max :
						max=float(detud[valeur])
	
			del detud
		conn.send("La note maxi de la matiere est %i\n" %max)
	elif data == "0":
		print "zero"
		for cle in dico_etud.keys():
			detud=dico_etud[cle]
			for valeur in detud.values():
				if float(valeur) > max:
					max=float(valeur)
			del detud
		conn.send("La note maxi de toutes les matieres de tout le monde est %i\n" %max)
		
	elif data in dico_etud.keys():
		print "etud"
		detud=dico_etud[data]
		for valeur in detud.values():
			if float(valeur) > max:
				max=float(valeur)
		del detud
		conn.send("La note maxi de l'etudiant est %i\n" %max)	
	else :
		conn.send("L'etudiant n'a pas ete trouve. Veuillez reessayer")
			
	

def reset(dico_etud):
	data = conn.recv(50)
	data=data.rstrip()
	if data == "0" :
		dico_etud.clear()
		conn.send("toutes les notes ont bien ete supprimees\n")
	if data == "matiere":
		matiere= conn.recv(50)
		matiere=matiere.rstrip()
		for cle in dico_etud.keys():
			detud=dico_etud[cle]
			for valeur in detud.keys():
				if valeur == matiere:
					del detud[valeur]
		conn.send("la matiere a bien ete supprimee\n")
	elif data in dico_etud.keys():
		del dico_etud[data]
		conn.send("les notes de la personne ont bien ete suprimees\n")
	else:
		conn.send("La personne n'est pas presente, la suppression ne se fait donc pas.\n")
	return dico_etud

def moyenne(dico_etud):
	data = conn.recv(50)
	data=data.rstrip()
	moy=0
	cpt=0
	if data == "matiere":
		matiere= conn.recv(50)
		matiere=matiere.rstrip()
		for cle in dico_etud.keys():
			detud=dico_etud[cle]
			for valeur in detud.keys():
				if valeur == matiere:
					cpt=cpt+1
					moy=moy+float(detud[valeur])
			del detud
		if cpt == 0 :
			conn.send("La matiere n'est pas presente, calcul impossible \n")
		else:
			moy=moy/cpt
			conn.send("La moyenne de la matiere est :%s \n" % moy)
		
	elif data == "0" :
		for cle in dico_etud.keys():
			detud=dico_etud[cle]
			cpt=cpt+len(detud)
			for valeur in detud.values():
				moy=moy+float(valeur)
			del detud
		moy=moy/cpt
		conn.send("Voici la moyenne de tous les etudiants dans toutes les matieres: %s \n" % moy)
	elif data in dico_etud.keys():
		detud=dico_etud[data]
		cpt=len(detud)
		for valeur in detud.values():
			moy=moy+float(valeur)
		moy=moy/cpt
		del detud
		conn.send("La moyenne de l'etudiant est : %s \n" % moy)
	else:
		conn.send("La personne n'est pas presente, la moyenne ne peut donc pas etre calculee.\n")
			
class ClientThread(Thread):

	def __init__(self,ip,port):
		Thread.__init__(self)
		self.ip=ip
		self.port=port
		print "[+] New thread started for "+ip+":"+str(port)
		conn.send(str(port));

	def run(self):
		dico_etud={}
		while True:
			data = conn.recv(BUFFER_SIZE)
			data=data.rstrip()
			data_separes=data.split(" ")
			if not data: break
			if data_separes[0] == 'UPLOAD' :
				print "upload!\n"
				dico_etud=upload(data_separes[1],data_separes[2],dico_etud)
				print "affichage !! \n"
				print dico_etud
			elif data_separes[0] =="MOYENNE" :
				print "moyenne"
				moyenne(dico_etud)
			elif data_separes[0] =="RESET" :
				print "reset\n"
				dico_etud=reset(dico_etud)
				print dico_etud
			elif data_separes[0] =="MIN" :
				print "min\n"
				min(dico_etud)
			elif data_separes[0] =="MAX" :
				print "max\n"
				max(dico_etud)



TCP_IP = '0.0.0.0'
TCP_PORT = 6265
BUFFER_SIZE = 100

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcpsock.bind((TCP_IP,TCP_PORT))
threads = []

while True:
	tcpsock.listen(4)
	print "waiting for incoming connections..."
	(conn,(ip,port)) = tcpsock.accept()
	newthread = ClientThread(ip,port)
	newthread.start()
	threads.append(newthread)
for t in threads:
	t.join()



		
		

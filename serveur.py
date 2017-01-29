#! /usr/bin/env python

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

def upload(connec, nombre_etudiants, module, dico_etud):
    print dico_etud
    for i in range(int(nombre_etudiants)):
        ligne = connec.recv(50)
        print ligne
        ligne = ligne.rstrip()
        ligne = ligne.split(";")
        if (ligne[0] in dico_etud.keys()):
            detud = dico_etud[ligne[0]]
            detud[module] = ligne[1]
        else:
            dico_tmp = {}
            dico_tmp[module] = ligne[1]
            dico_etud[ligne[0]] = dico_tmp
            del dico_tmp
    return dico_etud


def min(connec,dico_etud):
    data = connec.recv(50)
    data = data.rstrip()
    min = 20
    if "matiere" == data:
        print "matiere"
        matiere = connec.recv(50)
        matiere = matiere.rstrip()
        for cle in dico_etud.keys():
            detud = dico_etud[cle]
            for valeur in detud.keys():
                if valeur == matiere:
                    if float(detud[valeur]) < min:
                        min = float(detud[valeur])
            del detud
        connec.send("La note mini de la matiere est %i\n" % min)
    elif "0" == data:
        print "zero"
        for cle in dico_etud.keys():
            detud = dico_etud[cle]
            for valeur in detud.values():
                if float(valeur) < min:
                    min = float(valeur)
            del detud
        connec.send("La note mini de toutes les matieres de tout le monde est %i\n" % min)
    elif data in dico_etud.keys():
        print "etud"
        detud = dico_etud[data]
        for valeur in detud.values():
            if float(valeur) < min:
                min = float(valeur)
        del detud
        connec.send("La note mini de l'etudiant est %i\n" % min) 
    else :
        connec.send("L'etudiant n'a pas ete trouve. Veuillez reessayer")


def max(connec, dico_etud):
    data = connec.recv(50)
    data = data.rstrip()
    max = 0
    if "matiere" == data:
        print "matiere"
        matiere = connec.recv(50)
        matiere = matiere.rstrip()
        for cle in dico_etud.keys():
            detud = dico_etud[cle]
            for valeur in detud.keys():
                if valeur == matiere:
                    if float(detud[valeur]) > max :
                        max = float(detud[valeur])
            del detud
        connec.send("La note maxi de la matiere est %i\n" %max)
    elif "0" == data:
        print "zero"
        for cle in dico_etud.keys():
            detud = dico_etud[cle]
            for valeur in detud.values():
                if float(valeur) > max:
                    max = float(valeur)
            del detud
        connec.send("La note maxi de toutes les matieres de tout le monde est %i\n" % max)
    elif data in dico_etud.keys():
        print "etud"
        detud = dico_etud[data]
        for valeur in detud.values():
            if float(valeur) > max:
                max = float(valeur)
        del detud
        connec.send("La note maxi de l'etudiant est %i\n" % max) 
    else:
        connec.send("L'etudiant n'a pas ete trouve. Veuillez reessayer")


def reset(connec, dico_etud):
    data = connec.recv(50)
    data = data.rstrip()
    if "0" == data:
        dico_etud.clear()
        connec.send("Toutes les notes ont bien ete supprimees\n")
    if "matiere" == data:
        matiere = connec.recv(50)
        matiere = matiere.rstrip()
        for cle in dico_etud.keys():
            detud = dico_etud[cle]
            for valeur in detud.keys():
                if valeur == matiere:
                    del detud[valeur]
        connec.send("La matiere a bien ete supprimee\n")
    elif data in dico_etud.keys():
        del dico_etud[data]
        connec.send("Les notes de la personne ont bien ete suprimees\n")
    else:
        connec.send("La personne n'est pas presente, la suppression ne se fait donc pas.\n")
    return dico_etud


def moyenne(connec, dico_etud):
    data = connec.recv(50)
    data = data.rstrip()
    moy = 0
    cpt = 0
    if "matiere" == data:
        matiere = connec.recv(50)
        matiere = matiere.rstrip()
        for cle in dico_etud.keys():
            detud = dico_etud[cle]
            for valeur in detud.keys():
                if valeur == matiere:
                    cpt = cpt+1
                    moy = moy+float(detud[valeur])
            del detud
        if 0 == cpt:
            connec.send("La matiere n'est pas presente, calcul impossible \n")
        else:
            moy /= cpt
            connec.send("La moyenne de la matiere est :%s \n" % moy)
    elif "0" == data:
        for cle in dico_etud.keys():
            detud = dico_etud[cle]
            cpt += len(detud)
            for valeur in detud.values():
                moy += float(valeur)
            del detud
        moy /= cpt
        connec.send("Voici la moyenne de tous les etudiants dans toutes les matieres: %s \n" % moy)
    elif data in dico_etud.keys():
        detud = dico_etud[data]
        cpt = len(detud)
        for valeur in detud.values():
            moy += float(valeur)
        moy /= cpt
        del detud
        connec.send("La moyenne de l'etudiant est : %s \n" % moy)
    else:
        connec.send("La personne n'est pas presente, la moyenne ne peut donc pas etre calculee.\n")


class ClientThread(Thread):

    def __init__(self,ip,port,conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        print "[+] New thread started for "+ ip +":"+ str(port)
        self.conn.send(str(port));

    def run(self):
        dico_etud = {}
        while True:
            data = self.conn.recv(BUFFER_SIZE)
            data = data.rstrip()
            data_separes = data.split(" ")
            if not data: break
            if 'UPLOAD' == data_separes[0]:
                print "upload!\n"
                dico_etud = upload(self.conn, data_separes[1], data_separes[2], dico_etud)
                print "affichage !! \n"
                print dico_etud
            elif "MOYENNE" == data_separes[0]:
                print "moyenne"
                moyenne(self.conn,dico_etud)
            elif "RESET" == data_separes[0]:
                print "reset\n"
                dico_etud = reset(self.conn,dico_etud)
                print dico_etud
            elif "MIN" == data_separes[0]:
                print "min\n"
                min(self.conn, dico_etud)
            elif "MAX" == data_separes[0]:
                print "max\n"
                max(self.conn,dico_etud)



TCP_IP = '0.0.0.0'
TCP_PORT = 6265
BUFFER_SIZE = 100

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcpsock.bind((TCP_IP, TCP_PORT))

while True:
    tcpsock.listen(4)
    print "waiting for incoming connections..."
    (conn,(ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, conn)
    newthread.start()

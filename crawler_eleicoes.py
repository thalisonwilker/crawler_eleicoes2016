# -*- codin: latin1 -*-

from urllib2 import urlopen
import BeautifulSoup
from time import sleep
from sys import stderr

bs = BeautifulSoup.BeautifulSoup

from string import ascii_lowercase

class crawler_eleicoes_estaduais(object):
    cargo = 'prefeito'
    estado = 'pa'
    __url = 'https://www.eleicoes2016.com.br/candidatos-'+cargo+'-'+estado+'/'
    __muns = {}
    __total = 0

    def __init__(self, cargo=cargo,estado=estado):
        # type: (object, object) -> object
        self.cargo = cargo
        self.estado = estado
        
    def start(self):
        self.__load__()

    def __load__(self,url=__url):
        
        alfa = ascii_lowercase
        alfa = alfa.replace('h','')
        alfa = alfa.replace('k','')
        alfa = alfa.replace('w','')
        alfa = alfa.replace('y','')
        alfa = alfa.replace('z','')
        
        for letra in alfa:
            self.__url = 'https://www.eleicoes2016.com.br/candidatos-'+self.cargo+'-'+self.estado+'/'+str(letra)+"/"
            print 'Crawling',self.__url
            
            #print 'abrindo',self.__url
            
            code = urlopen(self.__url).read()
            html = bs(code)
            
            for municipio in html.findAll("ul",{"class":"custom"}):
                
                dados = bs(str(municipio))
                li = dados.findAll("li")

                for n in li:
                    
                    nome = n.a.getText()
                    n = n.span.getText()
                    n = n.split(" ")
                    n = n[0]
                    self.__total = self.__total + int(n)
                    self.__muns[nome] = int(n)

                    print nome,n

            print
            stderr.write("[*]Pausa pro lanche ")
            for x in range(5,0,-1):
                stderr.write(".")
                sleep(1)
            print
            stderr.write("[*] OK, GO!")
            print
            print

        self.__processa__()

    def __processa__(self):
        
        maior = []
        menor = []
        x = 0
        y = 100
        
        print 'processando...'
        for nome in self.__muns:
            
            if self.__muns[nome] >= x:
                x = self.__muns[nome]
                maior.append(x)
                
            elif self.__muns[nome] <= y:
                y = self.__muns[nome]
                menor.append(y)

        #print '[ maiores valores',maior,']'
        #print '[ menores valores',menor,']'

        print len(maior),'municipios possuem um maximo de',max(maior),'candidados para o cargo de',self.cargo
        print len(menor),'municipios possuem um maximo de',min(menor),'candidados para o cargo de',self.cargo
        print 'um total de',self.__total,'de candidatos para o cargo de',self.cargo,'em todo o estado de',self.estado.upper()

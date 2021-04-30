import math
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.patches as mpatches
import csv
#Metodo de los cuadrados

def dibujo(x,c):
	
	#for xi in x:
	#	plt.plot(x.index(xi),xi,'bo',alpha=0.1)
	for xi in range(0,len(x)-1):
		plt.plot(xi,x[xi],c,alpha=0.15)
	plt.ylim(min(x),max(x))

def dibujo_(x,c,nombre):
	plt.figure(figsize=(10,10))	
	plt.title(nombre)
	plt.xlabel("Corridas")
	plt.ylabel("Valor")
	for xi in range(0,len(x)-1):
		plt.plot(xi,x[xi],c,alpha=0.15)
	plt.ylim(min(x),max(x))
	plt.savefig(nombre+".svg")
	plt.close()	

def cuadrados():
	numeros = []
	semilla = str(6543)
	tam1 = len(semilla)
	
	numero1 = int(semilla)
	for i in range(1000):
		numero2 = numero1**2
		snumero2 = str(numero2)
		tam2 = len(snumero2)
		primerc = int((tam2 - tam1) / 2)
		snumero3 = snumero2[primerc:primerc+tam1]
		
		numero1 = int(snumero3)
		numeros.append(float("0."+str(numero1)))		
	dibujo(numeros,'bo')
	dibujo_(numeros,'bo',"Generador Cuadrados")
	
	tc = testCorridas(numeros)
	tp = testPoker(numeros)
	tch = TestChiCuadrado(numeros)
	tko = TestKolmogorov(numeros)

	
	csv_write("Tests Cuadrados.csv",tc+tp+tch+tko)


def congruente():
	x = []
	u = []
	
	x.append(6543)
	a = 7
	c = 0
	m = 512
	u.append(x[0]/m)
 
	for i in range(1,1000):
		x.append((a * x[i-1] + c) % m)
		u.append(x[-1]/m)
		
	
	u[0]=0.998046875
	dibujo(u,'ro')
	dibujo_(u,'ro',"Generador Congruente")

	tc = testCorridas(u)
	tp = testPoker(u)
	tch = TestChiCuadrado(u)
	tko = TestKolmogorov(u)


	csv_write("Tests Congruente.csv",tc+tp+tch+tko)


def gPython():
	x = []
	for i in range(1,1000):
		x.append(random.random())
	dibujo(x,'go')
	dibujo_(x,'go',"Generador Python")
	
	tc = testCorridas(x)
	#tp = testPoker(x)
	tch = TestChiCuadrado(x)
	tko = TestKolmogorov(x)


	csv_write("Tests Python.csv",tc+tch+tko)


def testCorridas(valoresGenerados):

	csv_file="Test_Corridas\n"
	corridas=0
	muestra=[]
	crece=[]
	decrece=[]
	for x in range(1,len(valoresGenerados)):
		if(valoresGenerados[x] <= valoresGenerados[x-1]):
			decrece.append(valoresGenerados[x])
			muestra.append(int(0))
		else:
			crece.append(valoresGenerados[x])
			muestra.append(int(1))
		if( x==1) :
			corridas=1
		else:
			if(muestra[x-1] != muestra[x-2]):
				corridas= corridas +1
	n1=len(crece)
	n2=len(decrece)
	media= ((2*n1*n2)/(n1+n2))+1
	var= ((2*n1*n2)*((2*n1*n2)-(n2+n1)) / (((n1+n2)**2)*(n1+n2+1)))

	csv_file = csv_file+"Varianza;"+str(var)+"\n"
	desvio= math.sqrt(var)

	csv_file = csv_file+"Desvio;"+str(desvio)+"\n"
	csv_file = csv_file+"Media;"+str(media)+"\n"


	cotaInferior= ((-1.96*desvio)+media)
	csv_file = csv_file+"Cota Inferior;"+str(cotaInferior)+"\n"

	cotaSuperior=((1.96*desvio)+media)
	csv_file = csv_file+"Cota superior;"+str(cotaSuperior)+"\n"
	csv_file = csv_file+"Resultado\n"
	if(corridas>=cotaInferior and corridas<=cotaSuperior):
		csv_file = csv_file + "Descripcion;Prueba no superada\n"
	else:
		csv_file = csv_file + "Descripcion;Prueba no superada\n"
	return csv_file

def testPoker(valores):
	csv_file = ""
	csv_file = csv_file + "Test Poker\n"
	xx = 0
	muestra=[]
	tiguales = 0
	dosiguales = 0
	tdistintos = 0
	ptiguales = 0.01
	pdosiguales = 0.27
	ptdistintos = 0.72
	for x in range (0,len(valores)):
		n=valores[x]
		n = round(n,3)
		muestra.append(n)

	longitudMuestra = len(muestra)
	for index in range (0,len(muestra)):
		i = 0
		numero=str(muestra[index])
		long=int(len(numero))
		numero= numero + '0'
		digito1=numero[2]
		digito2=numero[3]
		digito3=numero[4]
		if(digito1 == digito2 and digito2==digito3): ##1
			tiguales += 1
		elif(digito1!=digito2 and digito1!=digito3 and digito2!=digito3): ##2
			tdistintos += 1
		elif(digito1!=digito2 and digito2==digito3): ##3
			dosiguales += 1
		elif(digito1==digito2 and digito2 != digito3): ##4
			dosiguales += 1
		elif (digito1 != digito2 and digito1 == digito3):  ##5
			dosiguales += 1
		xx+=1	


    	
    
	csv_file = csv_file + "Iguales;"+str(tiguales)+"\n"
	csv_file = csv_file + "Distintos;"+str(tdistintos)+"\n"
	csv_file = csv_file + "Dos iguales;"+str(dosiguales)+"\n"
	
	FE1=ptiguales*longitudMuestra ## Frecuencia esperada de Todos iguales
	FE2=pdosiguales*longitudMuestra  ## Frecuencia esperada de solo 2 iguales
	FE3=ptdistintos*longitudMuestra ## Frecuencia esperada de Todos distintos
	x1=(((FE1-tiguales)**2) / FE1)
	x2=(((FE2-dosiguales)**2) / FE2)
	x3=(((FE3-tdistintos)**2) / FE3)
	poker=x1+x2+x3
	
	csv_file = csv_file + "Valor Poker;"+str(poker)+"\n"
	if(poker<=5.99):
		csv_file = csv_file + "Descripcion;Prueba superada\n"
	else:
		csv_file = csv_file + "Descripcion;Prueba no superada\n"
	return csv_file

def TestChiCuadrado(muestra):
	csv_file = ""
	csv_file = csv_file + "Test Chi\n"

	muestraAcotada = np.array(muestra)[1:100]
	n = muestraAcotada.__len__()
	c = round(math.sqrt(n))
	gl = c - 1
	fresperada = n/c 
	intervalos = calcularIntervalos(muestraAcotada)
	frobser = []
	for index in range(len(intervalos)):
		frobser.append(len(intervalos[index]))
	
	#chi
	valorChi = 0
	for yndex in range(len(frobser)):
		valorChi = valorChi + (((frobser[yndex] - fresperada)**2)/fresperada)
	
	csv_file = csv_file + "Valor Chi;"+str(valorChi)+"\n"
	if (valorChi > 16.92):
		csv_file = csv_file + "Descripcion;Prueba no superada\n"

	if (valorChi <= 16.92):
		csv_file = csv_file + "Descripcion;Prueba superada\n"
	return csv_file

def TestKolmogorov(muestra):
	csv_file = ""
	
	csv_file = csv_file + "Test Kolmogorov\n"
	muestraAcotada = np.array(muestra)[0: 100]
	n = len(muestraAcotada)
	gl = n #valor de la confianza
	confianza = 0.410 #Valor de confianza de un 95%
	intervalos = calcularIntervalos(muestraAcotada)
	probEsperadas = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
	diferencias = []
	fobs = []
	fobsAcum = []
	probsAcum = []
	acum = 0
	for index in range(len(intervalos)):
		fobs.append(len(intervalos[index]))
		acum = acum + len(intervalos[index])
		fobsAcum.append(acum)
		probsAcum.append(acum / 100)
	for index in range(len(probsAcum)):
		diferencias.append((probEsperadas[index] - probsAcum[index]))
	dmcalc = max(diferencias)
	
	csv_file = csv_file + "DM calculado;"+str(dmcalc)+"\nResultado Test;"+str(dmcalc)+"\n"
	if (dmcalc <= confianza):      
		csv_file = csv_file + "Descripcion;Superado\n"	      
	else:
		csv_file = csv_file + "Descripcion;No superado\n"
	return csv_file

def csv_write(path,csv_file):	
	text_file = open(path, "w")
	n = text_file.write(csv_file)
	text_file.close()   


def calcularIntervalos(muestra):
    intervalos = [[], [], [], [], [], [], [], [], [], []]
    for index in range(len(muestra)):
        num = muestra[index]
        if(num >= 0 and num <= 0.1): intervalos[0].append(num)
        elif(num > 0.1 and num <= 0.2): intervalos[1].append(num)
        elif(num > 0.2 and num <= 0.3): intervalos[2].append(num)
        elif(num > 0.3 and num <= 0.4): intervalos[3].append(num)
        elif(num > 0.4 and num <= 0.5): intervalos[4].append(num)
        elif(num > 0.5 and num <= 0.6): intervalos[5].append(num)
        elif(num > 0.6 and num <= 0.7): intervalos[6].append(num)
        elif(num > 0.7 and num <= 0.8): intervalos[7].append(num)
        elif(num > 0.8 and num <= 0.9): intervalos[8].append(num)
        elif(num > 0.9 and num <= 1): intervalos[9].append(num)
    return(intervalos)


#discretas
def dd_poisson(lam):
    x= 0
    b = math.exp((lam)* -1)
    tr = 1
    while b<tr:
        r = random.random()
        tr *= r
        if b<tr:
            x+1
    return x
def dd_hipergeometrica(tn,ns,p):
    x = 0
    s = 0
    for index in range(1,ns):
        r = random.random()
        if r<=p:
            s = 1
            x+=1
        else:
            s = 0
        p = ((tn * p) - s) / (tn - 1)
        tn-=1
    return x
def dd_binomial(n,p):
    x = 0
    for index in range (1,n):
        r = random.random()
        if p >= r:
            x+=1
    return x
def dd_pascal(k,q):
    tr = 1
    qr = math.log(q)
    for index in range(1,k):
        tr *= random.random()
    x = ( math.log(tr) ) / qr
    return x

#continuas
def dc_normal(ex,std):
    x = 0
    for index in range (1,12):
        x += random.random()
    x1 = std * (x - 6) + ex
    return x
def dc_gamma(k,a):
    tr = 1
    x = 0
    for index in range (1,k):
        tr *= random.random()
        x = ((math.log(tr)/a)* -1)
    return x
def dc_exponencial(e):
    r = random.random()
    x = e * -1 * math.log(r)
    return x
def dc_uniforme(a,b):
    r = random.random()
    x = a + (b - a) * r
    return x


ciclos = 100
poissons = []
exponenciales = []
gammas = []
normales = []
binomiales = []
pascales = []
hipergeometricos = [] 
uniformes = []

for x in range(ciclos):
    poissons.append(dd_poisson(10))
    hipergeometricos.append(dd_hipergeometrica(10,8,0.5))
    binomiales.append(dd_binomial(2,0.2))
    pascales.append(dd_pascal(4,5))

    normales.append(dc_normal(0,1))
    gammas.append(dc_gamma(10,2))
    exponenciales.append(dc_exponencial(2))
    uniformes.append(dc_uniforme(0,1))


dibujo_(poissons,'bo',"Distribucion de Poisson")
dibujo_(hipergeometricos,'bo',"Distribucion Hipergeometrica")
dibujo_(binomiales,'bo',"Distribucion binomial")
dibujo_(pascales,'bo',"Distribucion de Pascal")
dibujo_(normales,'bo',"Distribucion Normal")
dibujo_(gammas,'bo',"Distribucion Gamma")
dibujo_(exponenciales,'bo',"Distribucion exponencial")
dibujo_(uniformes,'bo',"Distribucion Uniforme")

gPython()



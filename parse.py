import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import time

# expressao regular pra remover a sujeira do campo da linha de onibus
linha_r = re.compile('[\t\n\r\-\|]+')

url = "http://www.pmf.sc.gov.br/servicos/index.php?pagina=onibus"

f = urllib2.urlopen(url)
doc = BeautifulSoup(f.read())
# print doc
EMPRESAS = {}
for e in doc.select('select[name="empresa"] > option'):
  if e.has_key("title"):
    nome = (e["title"].strip().encode("utf-8"), int(e["value"]))
    EMPRESAS[nome] = {}

def isTimeFormat(input):
  try:
    time.strptime(input, '%H:%M')
    return True
  except ValueError:
    return False

def busca_linhas(id,LINHAS):
  data = {
      "empresa":id,
      "opcao":1,
      "passoGeral":1,
      "passoEmpresa":1,
      }
  req = urllib2.Request(url, urllib.urlencode(data))
  doc = BeautifulSoup(urllib2.urlopen(req).read())
  for linha in doc.select('ul[class="listagem"] > li'):
    linha_data = linha_r.split(linha.contents[0].strip().encode("utf-8"))
    linha_numero = linha_data[0].strip()
    linha_nome = linha_data[1].strip()
    linha_url = "http://www.pmf.sc.gov.br/servicos/index.php?pagina=onibuslinha&idLinha="+linha_numero+"&menu=2"
    itinerario = busca_dados_linha_itinerario(linha_url)
    horaida = busca_dados_linha_horaida(linha_url)
    LINHAS[linha_nome] = {"nome":linha_nome,'empresa':empresa,'numero':linha_numero,"itinerario":itinerario,"horarios_ida":horaida}
    print LINHAS[linha_nome]

def busca_dados_linha_itinerario(url):
  # print url
  data = {"passoGeral":3}
  req = urllib2.Request(url, urllib.urlencode(data))
  doc = BeautifulSoup(urllib2.urlopen(req).read())
  itinerario = []
  for caminho in doc.select('ul[class="listagem"] > li'):
    itinerario.append(caminho.contents[0].strip().encode('utf-8')[3:])
  return itinerario

def busca_dados_linha_horaida(url):
  # print url
  data = {"passoGeral":1}
  req = urllib2.Request(url, urllib.urlencode(data))
  doc = BeautifulSoup(urllib2.urlopen(req).read())
  horarios = {"dias_uteis":[], "sabado":[], "domingo":[]}
  for horario in doc.select('td[valign="top"]')[1].contents[::2]:
    horarios["dias_uteis"].append(horario.strip())
  for horario in doc.select('td[valign="top"]')[2].contents[::2]:
    horarios["sabado"].append(horario.strip())
  for horario in doc.select('td[valign="top"]')[3].contents[::2]:
    horarios["domingo"].append(horario.strip())
  return horarios

LINHAS = {}
for empresa,id in EMPRESAS:
  # print empresa
  busca_linhas(id,LINHAS)
  # print urllib.urlencode({"empresa",
print EMPRESAS
print LINHAS

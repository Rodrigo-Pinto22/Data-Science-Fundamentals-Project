import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from datetime import datetime


stop_words = set(stopwords.words('portuguese'))


with open("C:\\Users\\ASUS\\Documents\\GitHub\\tutorial\\web_search_1", 'r') as f:
    df = pd.read_csv(f, delimiter= ',')


list_1,list_2, list_3, list_4, list_5, final_list = [], [], [], [], [], []

list_dates_1,list_dates_2,list_dates_3,list_dates_4,list_dates_5, final_list_dates = [], [], [], [], [], []


def remove_words(doc):
    return [word for word in doc if word.lower() not in stop_words]        

def numeric(f_doc):
    str_word = ""
    list_price = []
    price_pattern = r"\d{1}[.,]\d{3}"  #padrao do preço \b corresponde à ancora (limite da palavra) \d{1} um numero decimal [.,] ponto e virgula \d{3} tres numeros decimais
    for word in f_doc:
        str_word += word
    price = re.findall(price_pattern, str_word)
    return price

def fuel(g, fuel_text):
    lista_debug_1, lista_debug_1_, lista_debug_2, lista_debug_2_, lista_debug_2_a, lista_debug_2_aa, lista_debug_3, lista_debug_4, lista_debug_4_date, lista_debug_5, lista_debug_5_date = [], [], [], [], [], [], [], [], [], [], []
    i_1 =  i_2 =  i_3 = i_4 = i_5 = 0
    if g == 1:
        for word in fuel_text:
            i_1+=1
            if  word.lower() == "gasolina":
                word_n= fuel_text[i_1]
                lista_debug_1.append(word_n)
                lista_debug_1_ = numeric(lista_debug_1)
                for i in range(len(lista_debug_1_)):
                    lista_debug_1_[i] = float(lista_debug_1_[i])
                av = round(np.mean(lista_debug_1_),3)
                lista_debug_1_.clear()
                lista_debug_1_.append(av)
        return lista_debug_1_
    elif g ==2 :
        for word in fuel_text:
            i_2+=1
            if  word == "95":
                word_n= fuel_text[i_2+1]
                lista_debug_2.append(word_n)
                lista_debug_2_ = numeric(lista_debug_2)
                for i in range(len(lista_debug_2_)):
                    lista_debug_2_[i] = float(lista_debug_2_[i])
                av = round(np.mean(lista_debug_2_),3)
                lista_debug_2_.clear()
                lista_debug_2_.append(av)
                
        return  lista_debug_2_
    elif g == 3:
        for word in fuel_text:
            i_3+=1
            if  word == "Repsol" :#and fuel_text[i_3-1] == "/":
                word_1= fuel_text[i_3]
                word_2 = fuel_text[i_3+5]
                word_3 = fuel_text[i_3+10]
                i_3 = 0

                lista_debug_2_a.append(word_1)
                lista_debug_2_a.append(word_2)
                lista_debug_2_a.append(word_3)

                lista_debug_2_aa = numeric(lista_debug_2_a)
                for i in range(len(lista_debug_2_aa)):
                    lista_debug_2_aa[i] = float(lista_debug_2_aa[i])
                av = round(np.mean(lista_debug_2_aa),3)
                lista_debug_2_aa.clear()
                lista_debug_2_aa.append(av)
        return  lista_debug_2_aa
    elif g==4:
        for word in fuel_text:
            i_4+=1
            if word.lower() == "gasolina" and fuel_text[i_4].lower() == "especial" and fuel_text[i_4+1] == "95":
                word_4 = fuel_text[i_4+2]
                word_4_date = fuel_text[i_4+3]
                lista_debug_4.append(word_4)
                lista_debug_4 = numeric(lista_debug_4)
                lista_debug_4_date.append(word_4_date)
        return lista_debug_4, lista_debug_4_date
    elif g==5:
        for word in fuel_text:
            i_5+=1
            if word.lower()=="gasolina" and fuel_text[i_5]=="95":
                word_5 = fuel_text[i_5+1]
                word_5_date = fuel_text[i_5+2]
                lista_debug_5.append(word_5)
                lista_debug_5 = numeric(lista_debug_5)
                lista_debug_5_date.append(word_5_date)
        return lista_debug_5, lista_debug_5_date


a = 0
for i in range(0,len(df)):
    link = df.iloc[i,1]
    date = df.iloc[i,2]
    html = urlopen(link).read()
    soup = BeautifulSoup(html, features="html.parser")
    #print(f"{i}\n")
    #print()
    
    str_soup = str(soup)
    
    if str_soup.__contains__('Mais Gasolina'):
        
    #print(str_soup.__contains__('Preços de referência'))
    #print("------------------------------------------------------------------------------------------------")
        #print(soup)
        if str_soup[0:13]=="Mais Gasolina":
            
            if str_soup.__contains__('Preços de referência'):
                g = 1
                str_soup_1 = str_soup.split()               #Passar para lista, retirando os espaço entre palavras
                filtered_1 = remove_words(str_soup_1)       #Remover stopwords   
                fuel_soup_1 = fuel(g,filtered_1)            #Extrair possiveis preços
                list_1.extend(fuel_soup_1)                  #Guardar preços
                list_dates_1.append(date)                   #Guardar respectiva data do ficheiro 
                

            elif str_soup.__contains__("Comparador Galp / BP / Repsol"):
                str_soup_2 = str_soup.split()               
                g = 2            
                ###### Definir o índice onde começa e onde termina
                start_index = str_soup_2.index('Galp')
                end_index = 78+start_index
                #print(link)
                #print(str_soup_2[end_index])
                str_soup_2 = str_soup_2[start_index:end_index]
                # Extrair o subgrupo
                if str_soup_2[-1].endswith("operar"):       
                    filtered_2 = remove_words(str_soup_2)
                    #print(filtered_2)
                    fuel_soup_2 = fuel(g, filtered_2)
                    #print(fuel_soup_2)
                    #num_soup_gasolina_2 = numeric(fuel_soup_2)
                    list_2.extend(fuel_soup_2)
                    list_dates_2.append(date)
                    
                    
                else:                 
                    g = 3
                    filtered_2a = remove_words(str_soup_2)
                    #print(filtered_2a)
                    fuel_soup_2a = fuel(g, filtered_2a)
                    #print(fuel_soup_2a)
                    #num_soup_gasolina_2a = numeric(fuel_soup_2a)
                    list_2.extend(fuel_soup_2a)
                    list_dates_2.append(date)
                    if date == '2013-09-03':
                        print("Aqui")
                    
            else:          
                if str_soup.__contains__('Os mais baratos'):
                    #print(i)   
                    #print(str_soup)
                    #print()
                    #print("------------------------------------------3----------------------------------------------------- \n")
                    #print(link)
                    str_soup_3 = str_soup.split()
                    #print(str_soup_3)
                    #filtered = remove_words(str_soup)
                    #list_3.extend(filtered)
    else:
        
        if str_soup.__contains__('Gasóleo colorido') or str_soup.__contains__('Gasóleo especial') or str_soup.__contains__('Gasóleo simples') or str_soup.__contains__('Gasolina especial 98') or str_soup.__contains__('Gasolina simples 95'):
            str_soup_4 = str_soup.split()
            g = 4
            filtered_4 = remove_words(str_soup_4)
            start_index_4 = filtered_4.index('Última')
            end_index_4 = start_index + 50
            filtered_4 = filtered_4[start_index_4:end_index_4]
            fuel_soup_4, fuel_soup_4_date= fuel(g, filtered_4)
            list_4.extend(fuel_soup_4)
            list_dates_4.extend(fuel_soup_4_date)
        else:
            str_soup_5 = str_soup.split()
            g = 5
            filtered_5 = remove_words(str_soup_5)
            start_index_5 = filtered_5.index('Última')
            end_index_5 = start_index_5 + 50
            filtered_5 = filtered_5[start_index_5:end_index_5]
            fuel_soup_5, fuel_soup_5_date = fuel(g, filtered_5)
            list_5.extend(fuel_soup_5)
            list_dates_5.extend(fuel_soup_5_date)
            



print(list_dates_1)
print(f"lista 1 :{list_1}\n")
print(f"lista 2 :{list_2}\n")
print(list_dates_2)
print(len(list_2)%len(list_dates_2) == 0)
#print(f"lista 2 :{soup}\n")
#print(f"lista 3 :{list_3}\n")


list_comp = list_dates_4[:]
list_comp_price = list_4[:]
seen_price = set()
seen_date = set()
d = p = 0

for price, date in zip(list_4, list_dates_4):
    if date in seen_date and price in seen_price:
        list_comp.remove(date)
        list_comp_price.remove(price)

    elif date in seen_date and price not in seen_price:
        pass

    elif date not in seen_date and price in seen_price:
        pass

    else:
        seen_date.add(date)
        seen_price.add(price)

list_dates_4 = list_comp
list_4 = list_comp_price

for i in range(len(list_4)):
    word = list_4[i]
    word = word.replace(",",".")
    list_4[i] = float(word)
    
print(f"lista 4 :{list_4}\n")
print(f"lista 4 :{list_dates_4}\n")
print(len(list_4)%len(list_dates_4) == 0)

for i in range(len(list_5)):
    word = list_5[i]
    word = word.replace(",",".")
    list_5[i] = float(word)

print(f"lista 5 :{list_5}\n")
print(f"lista 5 :{list_dates_5}\n")
print(len(list_5)%len(list_dates_5) == 0)

for n in range(1,6):
    final_list.extend(eval(f"list_{n}"))
    final_list_dates.extend(eval(f"list_dates_{n}"))

print(f"Final list: \n", final_list)
print(f"\nFinal list for dates: \n", final_list_dates) 
print(f"Verification: ", len(final_list)%len(final_list_dates)==0 )

ziped = list(zip(final_list_dates, final_list))
ziped.sort()
final_list_dates, final_list = zip(*ziped)
final_list_dates = list(final_list_dates)
final_list = list(final_list)

dict_price = {'Price': final_list, 
              'Date': final_list_dates}

print(dict_price)

# Converter as datas de string para objetos datetime
update_final_lst_date = [datetime.strptime(data, '%Y-%m-%d') for data in final_list_dates]

# Plotar o gráfico
"""plt.figure(figsize=(10, 5))
plt.plot(update_final_lst_date, final_list, marker='o', color='b', linestyle='-')
plt.title('Evolução do Preço ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

"""Fazer depois um gráfico com os dados que tenho"""

#pequena alteracao 
f.close()
import re


def Confirm_if_name_empty(name):
    n = len(name)
    if n <= 0:
    # if name == '':
        cor_nome = 'red'
        return cor_nome
    else:
        cor_nome = 'green'
        return cor_nome
    

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
def Confirm_if_email(email):
    if(re.fullmatch(regex, email)):
        cor = 'green'
        return cor
    else:
        cor = 'red'
        return cor


def Confirm_if_pass_empty(senha):
    n = len(senha)
    if n <= 0:
        cor_senha = 'red'
        return cor_senha
    else:
        cor_senha = 'green'
        return cor_senha


           
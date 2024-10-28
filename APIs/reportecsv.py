import pandas as pd
from connect import create_connect

dataBase = r'../BDinscricao'
conn = create_connect(dataBase)

        ## cria um exel com todos
query = """
        select id, nome, datanas as dataNascimento, telefone, case membro when 'true' then 'sim' else 'não' end membro, case presenca when '0' then 'nao' else 'sim' end presente
        from inscricao
        union
        select id, nome, datanas as dataNascimento, telefone, case membro when 'true' then 'sim' else 'não' end membro, case presenca when '0' then 'nao' else 'sim' end presente
        from dependente  
"""
df = pd.read_sql_query(query, conn)

df.to_excel('inscricaoevento.xlsx', sheet_name='inscricao', index=False, header=True) 

        ## crianças
# query = """
#         select id, nome, datanas as dataNascimento, telefone, case membro when 'true' then 'sim' else 'não' end membro
#         from inscricao 
#         where substr(datanas,7,4) BETWEEN '2016' and '2020'  
#         union
#         select id, nome, datanas as dataNascimento, telefone, case membro when 'true' then 'sim' else 'não' end membro
#         from dependente
#         where substr(datanas,7,4) BETWEEN '2016' and '2020'  
# """

# df = pd.read_sql_query(query, conn)

# df.to_excel('criancas.xlsx', index=False, header=True)
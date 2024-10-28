from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from connect import execute_insert, create_connect, execute_query
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return "pong"

@app.post("/inscricao")
async def inscricao(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    data = json.loads(retorno)
    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)

    queryselect = f"""
        select b.id, b.nome
        from inscricao b 
        where b.telefone = "{data['telefone']}"
    """
    retorno = execute_query(conn, queryselect)
    if len(retorno) > 0:
        retnome = str(retorno[0][1])
        datnome = str(data["nome"])
        if retnome != datnome:
            msg = {"nome": retorno[0][1], "id": retorno[0][0], "erro": 2}  # Erro 2 = ja existe cadastro da pessoa na tabela
            msg = json.dumps(msg) 
            print(msg)   
            conn.close()
            return msg
    else:
        queryselect = f"""
            select b.id, b.nome
            from dependente b 
            where b.telefone = "{data['telefone']}"
        """
        retorno = execute_query(conn, queryselect)
        if len(retorno) > 0:
            retnome = str(retorno[0][1])
            datnome = str(data["nome"])
            if retnome != datnome:
                msg = {"nome": retorno[0][1], "id": retorno[0][0], "erro": 2}  # Erro 2 = ja existe cadastro da pessoa na tabela
                msg = json.dumps(msg) 
                print(msg)   
                conn.close()
                return msg

    queryselect = f"""
        select b.nome 
        from dependente a, 
             inscricao b 
        where a.telefone = "{data['telefone']}"
        AND a.idpai = b.id 
    """
    retorno = execute_query(conn, queryselect)
    if len(retorno) > 0:
        msg = {"nome": retorno[0][0], "id": 0, "erro": 1}  # Erro 1 = ja existe cadastro da pessoa no dependente
        msg = json.dumps(msg) 
        print(msg)   
        conn.close()
        return msg
        
    queryselect = f"""
        select id, nome 
        from inscricao
        where telefone = "{data['telefone']}"
    """
    linhas = execute_query(conn, queryselect)
    msg = 0
    if len(linhas) == 0:
        query = f"""
            insert into inscricao (nome, datanas, telefone, membro, presenca)
            VALUES("{data['nome']}","{data['datanas']}","{data['telefone']}","{data['membro']}", 0)
            """
        execute_insert(conn, query)
        
        retorno = execute_query(conn, queryselect)
        msg = {"id": retorno[0][0], "nome": retorno[0][1], "erro": 0} # Erro 0 = Registro inserido com sucesso
        msg = json.dumps(msg)
        print(msg)
    else:
        query = f"""
            select id, nome 
            from inscricao
            where telefone = "{data['telefone']}"
            """
        execute_query(conn, query)
        
        retorno = execute_query(conn, query)
        msg = {"id": retorno[0][0], "nome": retorno[0][1], "erro": 0} # Erro 0 = Registro consultado
        msg = json.dumps(msg)      
    
    conn.close()
             
    return msg

@app.post("/dependente")
async def dependente(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    data = json.loads(retorno)
    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)
    # queryselect = f"""
    #     select id, nome
    #     from inscricao
    #     where telefone = "{data['telefone']}"
    # """
    # linhas = execute_query(conn, queryselect)
    # if len(retorno) > 0:
    #     msg = {"nome": retorno[0][0], "id": 0}
    #     msg = json.dumps(msg) 
    #     print(msg)   
    #     conn.close()
             
    #     return msg  
    
    queryselect = f"""
        select id, nome
        from dependente
        where idpai = "{data['idPai']}" and nome = "{data['nome']}"
    """
    linhas = execute_query(conn, queryselect)
    if len(linhas) == 0:
        query = f"""
            insert into dependente (idpai, nome, datanas, telefone, membro, presenca)
            VALUES("{data['idPai']}","{data['nome']}","{data['datanas']}","{data['telefone']}","{data['membro']}", 0)
            """
        execute_insert(conn, query)
        queryselect = f"""
        select id, nome
        from dependente
        where idpai = "{data['idPai']}"
        """
        retorno = execute_query(conn, queryselect)
        idx = 0
        msg = "["
        for item in retorno:
            idx += 1
            msg += '{"id":' + f"{item[0]}" + ', "nome":"' + f"{item[1]}" + '"}'
            if idx < len(retorno):
                msg += ','
        msg += "]"
        print(msg)
    else:
        queryselect = f"""
        select id, nome
        from dependente
        where idpai = "{data['idPai']}"
        """
        retorno = execute_query(conn, queryselect)
        idx = 0
        msg = "["
        for item in retorno:
            idx += 1
            msg += '{"id":' + f"{item[0]}" + ', "nome":"' + f"{item[1]}" + '"}'
            if idx < len(retorno):
                msg += ','
        msg += "]"
        print(msg)

    conn.close()
    return msg


@app.post("/procuradep")
async def procuradep(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    data = json.loads(retorno)
    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)
    queryselect = f"""
        select id, nome
        from dependente
        where idpai = "{data['idPai']}"
        """
    retorno = execute_query(conn, queryselect)
    idx = 0
    msg = "["
    for item in retorno:
        idx += 1
        msg += '{"id":' + f"{item[0]}" + ', "nome":"' + f"{item[1]}" + '"}'
        if idx < len(retorno):
            msg += ','
    msg += "]"
    print(msg)
    
    conn.close()
    return msg


@app.post('/recepcao')
async def recpcao(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    req = json.loads(retorno)

    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)

    for pessoa in req:
        if pessoa['idpai'] == 0:
            query = f'UPDATE inscricao SET presenca = {pessoa["presenca"]} WHERE id = {pessoa["id"]}'
        else:
            query = f'UPDATE dependente SET presenca = {pessoa["presenca"]} WHERE id = {pessoa["id"]}'
        retorno = execute_query(conn, query)
        print(query)

    query = 'commit'
    retorno = execute_query(conn, query)

    conn.close()
    return 'OK'


@app.get('/buscaPessoas')
async def recpcao(request: Request):
    retorno = await request.body()
    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)

    queryselect = f"""
        select id, nome, presenca
          from inscricao
          order by nome
        """
    
    totalinscritos = 0
    totalmenores = 0
    msg = []
    inscritos = execute_query(conn, queryselect)
    if(len(inscritos) > 0):
        for inscrito in inscritos:
            ret = {}
            ret['id'] = inscrito[0]
            ret['nome'] = inscrito[1]
            ret['presenca'] = inscrito[2]
            ret['idpai'] = 0
            ret['pai'] = True
            msg.append(ret)
            totalinscritos += 1

            queryselect = f"""
                select id, nome, presenca, idpai, datanas
                  from dependente 
                 where idpai = {inscrito[0]}
                 order by nome
                """
            
            dependentes = execute_query(conn, queryselect)

            if(len(dependentes) > 0 ):
                for dependente in dependentes:
                    dep = {}
                    dep['id'] = dependente[0]
                    dep['nome'] = dependente[1]
                    dep['presenca'] = dependente[2]
                    dep['idpai'] = dependente[3]
                    dep['pai'] = False
                    msg.append(dep)

                    datanascimento = int(dependente[4][6:10] + dependente[4][3:5] + dependente[4][0:2])
                    if datanascimento >= 20201025 and datanascimento <= 20230425:
                        totalmenores += 1
                    if datanascimento < 20201025:
                        totalinscritos += 1

                        # 25/10/2020 - 25/04/2023

        ret = {}
        ret['id'] = 0
        ret['nome'] = 'Total'
        ret['presenca'] = 0
        ret['idpai'] = totalinscritos
        ret['pai'] = totalmenores
        msg.append(ret)

# todos os registros em orden alfabética

    # queryselect = f"""
    #     select * 
    #     from ( 
    #         select id, nome, presenca, 0 as idpai, 1 as pai
    #         from inscricao a
    #         union
    #         select id, nome, presenca, idpai, 0 as pai
    #         from dependente d 
    #         )
    #     order by nome
    #     """
   
    # msg = []
    # inscritos = execute_query(conn, queryselect)
    # if(len(inscritos) > 0):
    #     for inscrito in inscritos:
    #         ret = {}
    #         ret['id'] = inscrito[0]
    #         ret['nome'] = inscrito[1]
    #         ret['presenca'] = inscrito[2]
    #         ret['idpai'] = inscrito[3]
    #         ret['pai'] = inscrito[4]
    #         msg.append(ret)

    # print(msg)

    conn.close()
    return msg    

@app.get('/totalinscritos')
async def totalinscritos(request: Request):
    retorno = await request.body()
    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)

    queryselect = f"""
        select count(*) total from inscricao
        """

    totinscritos = 0
    inscritos = execute_query(conn, queryselect)
    if(len(inscritos) > 0):
        for inscrito in inscritos:        
            totinscritos += int(inscrito[0])

    queryselect = f"""
        select count(*) from (
        select substr(datanas,7,4) || substr(datanas,4,2) || substr(datanas,1,2) as datacompleta 
        from dependente 
        where datacompleta < '20201025' 
        )
        """

    dependentes = execute_query(conn, queryselect)
    if(len(dependentes) > 0):
        for dependente in dependentes:
            totinscritos += int(dependente[0])

    ret = {}
    ret['totalinscritos'] = totinscritos

    return ret

@app.post("/filaespera")
async def filaespera(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    data = json.loads(retorno)
    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)

    # Rotina para quando o telefone ficar em branco

    if(len(data['telefone']) == 0):

        queryselect = f"""
            select b.id, b.nome
            from filaespera b 
            where b.nome = "{data['nome']}"
        """
        retorno = execute_query(conn, queryselect)
        if len(retorno) > 0:
            retorno = execute_query(conn, queryselect)
            msg = {"id": retorno[0][0], "nome": retorno[0][1], "erro": 0} # Erro 0 = Registro inserido com sucesso
            msg = json.dumps(msg)
            conn.close()
            return msg

        query = f"""
            insert into filaespera (nome, datanas, telefone, membro)
            VALUES("{data['nome']}","{data['datanas']}","{data['telefone']}","{data['membro']}")
            """
        execute_insert(conn, query)

        queryselect = f"""
            select b.id, b.nome
            from filaespera b 
            where b.nome = "{data['nome']}"
        """
        
        retorno = execute_query(conn, queryselect)
        msg = {"id": retorno[0][0], "nome": retorno[0][1], "erro": 0} # Erro 0 = Registro inserido com sucesso
        msg = json.dumps(msg)

        conn.close()
        return msg

    # Rotina de inserção ou consulta para cadastro completo com telefone

    queryselect = f"""
        select b.id, b.nome
        from filaespera b 
        where b.telefone = "{data['telefone']}"
    """
    retorno = execute_query(conn, queryselect)
    if len(retorno) > 0:
        retnome = str(retorno[0][1])
        datnome = str(data["nome"])
        if retnome != datnome:
            msg = {"nome": retorno[0][1], "id": retorno[0][0], "erro": 2}  # Erro 2 = ja existe cadastro da pessoa com o telefone
            msg = json.dumps(msg) 
            print(msg)   
            conn.close()
            return msg
    # else:
    #     queryselect = f"""
    #         select b.id, b.nome
    #         from dependente b 
    #         where b.telefone = "{data['telefone']}"
    #     """
    #     retorno = execute_query(conn, queryselect)
    #     if len(retorno) > 0:
    #         retnome = str(retorno[0][1])
    #         datnome = str(data["nome"])
    #         if retnome != datnome:
    #             msg = {"nome": retorno[0][1], "id": retorno[0][0], "erro": 2}  # Erro 2 = ja existe cadastro da pessoa na tabela
    #             msg = json.dumps(msg) 
    #             print(msg)   
    #             conn.close()
    #             return msg

    # queryselect = f"""
    #     select b.nome 
    #     from dependente a, 
    #          inscricao b 
    #     where a.telefone = "{data['telefone']}"
    #     AND a.idpai = b.id 
    # """
    # retorno = execute_query(conn, queryselect)
    # if len(retorno) > 0:
    #     msg = {"nome": retorno[0][0], "id": 0, "erro": 1}  # Erro 1 = ja existe cadastro da pessoa no dependente
    #     msg = json.dumps(msg) 
    #     print(msg)   
    #     conn.close()
    #     return msg
        
    queryselect = f"""
        select id, nome 
        from filaespera
        where telefone = "{data['telefone']}"
    """
    linhas = execute_query(conn, queryselect)
    msg = 0
    if len(linhas) == 0:
        query = f"""
            insert into filaespera (nome, datanas, telefone, membro)
            VALUES("{data['nome']}","{data['datanas']}","{data['telefone']}","{data['membro']}")
            """
        execute_insert(conn, query)
        
        retorno = execute_query(conn, queryselect)
        msg = {"id": retorno[0][0], "nome": retorno[0][1], "erro": 0} # Erro 0 = Registro inserido com sucesso
        msg = json.dumps(msg)
    else:
        query = f"""
            select id, nome 
            from filaespera
            where telefone = "{data['telefone']}"
            """
        execute_query(conn, query)
        
        retorno = execute_query(conn, query)
        msg = {"id": retorno[0][0], "nome": retorno[0][1], "erro": 0} # Erro 0 = Registro consultado
        msg = json.dumps(msg)      
    
    conn.close()

    return msg

@app.get('/totalcriancas')
async def totcriancas(request: Request):
    retorno = await request.body()
    dataBase = r'../BDinscricao'
    conn = create_connect(dataBase)

    queryselect = f"""
        select count(*) total from (
        select nome, datanas, substr(datanas,7,4) || substr(datanas,4,2) || substr(datanas,1,2) as datacompleta 
        from inscricao d
        ) ret
        where ret.datacompleta BETWEEN '20201025' and '20230425'
        """
    totalcriancas = 0
    inscritos = execute_query(conn, queryselect)
    if(len(inscritos) > 0):
        for inscrito in inscritos:
            totalcriancas += inscrito[0]
    
    queryselect = f"""
        select count(*) total from (
        select nome, datanas, substr(datanas,7,4) || substr(datanas,4,2) || substr(datanas,1,2) as datacompleta 
        from dependente d
        ) ret
        where ret.datacompleta BETWEEN '20201025' and '20230425'
        """
    inscritos = execute_query(conn, queryselect)
    if(len(inscritos) > 0):
        for inscrito in inscritos:
            totalcriancas += inscrito[0]

    if totalcriancas > 15:
        msg = {"erro": 3} # Erro 3 = Limite máximo de Crianças alcançadas
        msg = json.dumps(msg) 
    else:
        msg = {"erro": 0} # Erro 0 = Registro inserido com sucesso
        msg = json.dumps(msg) 
        
    conn.close()

    return msg
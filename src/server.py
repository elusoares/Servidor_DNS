# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import socket

IP = "172.17.101.153"
PORT = 50001

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.bind((IP, PORT))
connection.listen(1)
print "Servidor em execucao, ouvindo em ",IP,":",PORT



while 1:    
    conn, addr = connection.accept()
    print "Conexao recebida vindo do IP: ",addr
    dataFromClient = conn.recv(2048) #recebe a requisicao do cliente
    
    try:
        dataFromClient = dataFromClient.split(".") #dividindo a mensagem que veio do cliente
        siteType = dataFromClient[0] #pega o tipo do site: www, portal ou mail
        url = ""
        for x in dataFromClient: #CONSERTAR AQUI, TENHO QUE PERCORRER A PARTIR DO SEGUNDO ELEMENTO DE DATAFROMCLIENT
            if url == "":
                url = x
            else:
                url = "." + x
        
        fileDns = file('dns.conf') #abre o arquivo dns
        
        verifySiteName = False #para verificar se o nome do site eh mesmo verdadeiro. Por exemplo, face.com nao eh o mesmo que facebook.com. Face estah contido em Facebook
        for line in fileDns: #percorre o arquivo dns
            #if dataFromClient[1] in line: #se em alguma linha contiver o nome do site procurado
            if url in line: #se em alguma linha contiver o nome do site procurado
                fileName = line.split(' ') #separa a linha utilizando o delimitador espaco em branco
                #fileName[0] = fileName[0].split('.') #agora separa a primeira parte do que foi separado no comando anterior utilizando o delimitador ponto (.)
                #if fileName[0][1] == dataFromClient[1]: #se o nome principal do site for igual ao nome principal do endereco mandado pelo cliente
                if fileName[0] == url: #se o nome do site for igual ao endereco mandado pelo cliente
                    verifySiteName = True #atribui-se verdadeiro 
                    
        if verifySiteName: #se for verdadeiro
            fileName = fileName[1] #mantem-se apenas a segunda parte da separacao resultante
            fileName = fileName[0:len(fileName)-1] #exclui-se o ultimo caractere dessa string que eh o \n
            fileName += ".conf" #adiciona-se .conf para completar o nome do arquivo

            fileSite = file(fileName) #abre-se o arquivo do site

            reply = ""
            
            verifySiteType = False #para verificar o tipo do site (mail, portal, www)
            for content in fileSite: #percorre o arquivo com os ips do site
                content = content.split(' ')#divide o conteudo para verificar
                if content[0] == siteType:#se o endereco que o cliente mandou foi www.blabla, entao manda de volta o email referente a www. Se foi mail.blabla, manda de volta o ip correspondente a mail
                    reply = content[1] #junta tudo numa string 
                    verifySiteType = True
                    
            if verifySiteType:
                conn.sendall(reply)#envia para o cliente
            else:#se nao for verdadeiro
                raise IOError #lanca uma excecao
                
        else: #se nao for verdadeiro
            raise IOError #lanca uma excecao

        
    except IOError: #se pegar essa excecao
        conn.sendall("Endereco nao encontrado")#entao o sistema trata o erro informando ao cliente que o endereco nao existe
    finally:
        conn.close()

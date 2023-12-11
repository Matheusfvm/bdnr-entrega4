from datetime import datetime
import json
import uuid
import servicos.produto as produto
import servicos.usuario as usuario

def criarCompra(conexaoCassandra):
    dataCompra = datetime.now()
    dataCompraFormatada = dataCompra.strftime("%d/%m/%Y %H:%M")
    listaProduto = []
    valortotalCompra = 0
    key = "S"
    while key == "S":
        quantidadeProdutoCompra = int(input("Quantidade de produto: "))        
        produtoEscolhido = produto.consultaProduto(conexaoCassandra)
        produtoObjeto = {
            "descricao": produtoEscolhido["descricao"],
            "preco": produtoEscolhido["preco"],
            "quantidadeProdutoCompra": quantidadeProdutoCompra,
            "vendedor": produtoEscolhido["vendedor"] 
        }
        listaProduto.append(produtoObjeto)    
        valortotalCompra += produtoEscolhido["preco"] * quantidadeProdutoCompra    
        key = str(input("Deseja comprar um outro produto(S/N)? "))
    dataCompraEntrega = str(input("Data da entrega(dd/mm/AAAA): "))
    listaNomeEmailUsuario = usuario.vinculaCompraUsuario(listaProduto, dataCompraEntrega, dataCompraFormatada, valortotalCompra)  
    usuarioObjeto = {
        "nome": listaNomeEmailUsuario[0],
        "cpf": listaNomeEmailUsuario[1]
    }
    jsonUsuario = json.dumps(usuarioObjeto)
    jsonListaCompra = json.dumps(listaProduto)
    conexaoCassandra.execute(
        '''INSERT INTO compra (id, datacompra, dataentrega, usuario, listaproduto, valortotal) 
        VALUES (%s, %s, %s, %s, %s, %s);''', 
        (uuid.uuid4(), dataCompraFormatada, dataCompraEntrega, jsonUsuario, jsonListaCompra, valortotalCompra)
    )
    print(f'\nCompra realizada com sucesso!\n')

def listarCompras(conexaoCassandra):    
    listaCompra = conexaoCassandra.execute("SELECT * FROM compra;")    
    for compra in listaCompra:
        indiceCompra = 1
        objetoUsuarioCompra = json.loads(compra['usuario'])
        print(f"\n{indiceCompra}º Compra\n")
        print(f"CPF do usuário: {objetoUsuarioCompra['cpf']}")
        print(f"Data e hora da compra: {compra['datacompra']}")
        print(f"Data entrega: {compra['datacompraentrega']}\n")
        print(f"Valor total da compra: R${compra['valortotal']:.2f}")
        print("\nProdutos\n")
        for produto in compra['listaproduto']:
            objetoProdutoCompra = json.loads(produto)
            print(f"Descrição: {produto['descricao']}")
            print(f"Preço: {produto['preco']:.2f}")
            print(f"Quantidade: {produto['quantidadeProdutoCompra']}")
            print("\n---------------------------------------\n")
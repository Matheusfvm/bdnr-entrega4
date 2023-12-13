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
        produtoEscolhido = produto.consultaProduto(conexaoCassandra)
        quantidadeProdutoCompra = str(input("Quantidade de produto: "))
        while True:
            if quantidadeProdutoCompra.isnumeric():
                quantidadeProdutoCompraValidada = int(quantidadeProdutoCompra)
                break
            else:
                print("\nDigite um número inteiro!\n")
                quantidadeProdutoCompra = str(input("Digite a quantidade: "))        
        objetoVendedorProduto = json.loads(produtoEscolhido['vendedor'])
        produtoObjeto = {
            "descricao": produtoEscolhido["descricao"],
            "preco": produtoEscolhido["preco"],
            "quantidadeProdutoCompra": quantidadeProdutoCompraValidada,
            "vendedor": objetoVendedorProduto
        }
        listaProduto.append(produtoObjeto)    
        valortotalCompra += produtoEscolhido["preco"] * quantidadeProdutoCompraValidada    
        key = str(input("Deseja comprar um outro produto(S/N)? "))
    dataCompraEntrega = str(input("Data da entrega(dd/mm/AAAA): "))
    listaNomeEmailUsuario = usuario.vinculaCompraUsuario(listaProduto, dataCompraEntrega, dataCompraFormatada, valortotalCompra, conexaoCassandra)  
    usuarioObjeto = {
        "nome": listaNomeEmailUsuario[0],
        "cpf": listaNomeEmailUsuario[1]
    }
    jsonUsuarioCompra = json.dumps(usuarioObjeto)
    jsonListaCompra = json.dumps(listaProduto)
    conexaoCassandra.execute(
        '''INSERT INTO compra (id, datacompra, dataentrega, usuario, listaproduto, valortotal) 
        VALUES (%s, %s, %s, %s, %s, %s);''', 
        (uuid.uuid4(), dataCompraFormatada, dataCompraEntrega, jsonUsuarioCompra, jsonListaCompra, valortotalCompra)
    )
    print(f'\nCompra realizada com sucesso!\n')

def listarCompras(conexaoCassandra):    
    listaCompra = conexaoCassandra.execute("SELECT * FROM compra;")
    indiceCompra = 1  
    for compra in listaCompra:
        compra = compra._asdict()
        print(f"\n{indiceCompra}º Compra\n")
        print(f"Data e hora da compra: {compra['datacompra']}")
        print(f"Data entrega: {compra['dataentrega']}")
        print(f"Valor total da compra: R${compra['valortotal']:.2f}")
        print("\nProdutos\n")
        objetoProdutoCompra = json.loads(compra['listaproduto'])
        indiceCompra += 1
        for produto in objetoProdutoCompra:
            print(f"Documento do vendedor: {produto['vendedor']['documento']}")
            print(f"Descrição: {produto['descricao']}")
            print(f"Preço: {produto['preco']:.2f}")
            print(f"Quantidade: {produto['quantidadeProdutoCompra']}")
            print("\n---------------------------------------\n")
            
import json
import servicos.vendedor as vendedor


def criarProduto(conexaoCassandra):
    while True:
        descricao = str(input("Descrição: "))
        produtoEscolhido = conexaoCassandra.execute("SELECT * FROM produto WHERE descricao = %s;", (descricao,))
        if not produtoEscolhido:
            break
        else:
            print("\nProduto já cadastrado!")
            print("Digite outra descrição!\n")            
    preco = str(input("Preço(R$): "))
    while True:
        validacao = is_float(preco)
        if validacao:
            precoValidado = float(preco)
            break
        else:
            print("\nDigite uma valor valido!\n")
            preco = str(input("Digite o preço(R$): "))
    quantidadeProduto = str(input("Quantidade: "))
    while True:
        if quantidadeProduto.isnumeric():
            quantidadeValidada = int(quantidadeProduto)
            break
        else:
            print("\nDigite um número inteiro!\n")
            quantidadeProduto = str(input("Digite a quantidade: "))
    listaNomeDocumentoVendedor = vendedor.vinculaProdutoVendedor(descricao, preco, quantidadeProduto, conexaoCassandra)
    if listaNomeDocumentoVendedor != True:
        vendedorObjeto = {
        "nome": listaNomeDocumentoVendedor[0],
        "documento": listaNomeDocumentoVendedor[1]
        }
        jsonVendedorProduto = json.dumps(vendedorObjeto)
        conexaoCassandra.execute(
            '''INSERT INTO produto (descricao, preco, quantidade, vendedor) 
            VALUES (%s, %s, %s, %s);''', 
            (descricao, precoValidado, quantidadeValidada, jsonVendedorProduto)
            )    
        print(f'\nProduto cadastrado com sucesso!\n')

def atualizarProduto(conexaoCassandra):
    objetoProdutoEscolhido = consultaProduto(conexaoCassandra)
    novoPreco = str(input("Digite o novo preço(R$): "))
    while True:
        validacao = is_float(novoPreco)
        if validacao:
            novoPrecoValidado = float(novoPreco)
            break
        else:
            print("Digite uma valor valido!")
            novoPreco = str(input("Digite o novo preço(R$): "))
    novaQuantidade = str(input("Digite a nova quantidade: "))
    while True:
        if novaQuantidade.isnumeric():
            novaQuantidadeValidada = int(novaQuantidade)
            break
        else:
            print("Digite um número inteiro!")
            novaQuantidade = str(input("Digite a nova quantidade: "))
    conexaoCassandra.execute(
        "UPDATE produto SET preco = %s, quantidade = %s WHERE descricao = %s;", 
        (novoPrecoValidado, novaQuantidadeValidada, objetoProdutoEscolhido['descricao']))
    print(f'\nProduto {objetoProdutoEscolhido["descricao"]} atualizado com sucesso!\n')        

def deletarProduto(conexaoCassandra):
    objetoProdutoEscolhido = consultaProduto(conexaoCassandra)
    conexaoCassandra.execute(
        "DELETE FROM produto WHERE descricao = %s;",
        (objetoProdutoEscolhido['descricao'],)
        )
    print(f'\nO produto {objetoProdutoEscolhido["descricao"]} foi deletado com sucesso!\n')

def listarProduto(conexaoCassandra):
    produtoEscolhido = consultaProduto(conexaoCassandra)
    objetoVendedor = json.loads(produtoEscolhido['vendedor'])
    print("\nProduto")
    print(f"\nDescrição: {produtoEscolhido['descricao']}")
    print(f"Preço: R${produtoEscolhido['preco']:.2f}")
    print(f"Quantidade: {produtoEscolhido['quantidade']}")
    print("\nVendedor\n")
    print(f"Nome: {objetoVendedor['nome']}")
    print(f"Documento: {objetoVendedor['documento']}")


def consultaProduto(conexaoCassandra):
    while True:
        descricao = str(input("Descrição do produto: "))
        produtoEscolhido = conexaoCassandra.execute("SELECT * FROM produto WHERE descricao = %s;", (descricao,))
        if not produtoEscolhido:
            print("Nenhum produto encontrado")                    
        else:            
            objetoProdutoEscolhido = produtoEscolhido.one()._asdict()
            break  
    return objetoProdutoEscolhido

def is_float(texto):
    try:
        float(texto)
        return True
    except ValueError:
        return False
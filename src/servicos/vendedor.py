import json


def criarVendedor(conexaoCassandra):
    nome = str(input("Nome: "))
    while True:
        documento = str(input("Documento: "))
        vendedorEscolhido = conexaoCassandra.execute("SELECT * FROM vendedor WHERE documento = %s;", (documento,))
        if not vendedorEscolhido:
            break
        else:
            print("Já exite um vendedor cadastrado com esse documento!")        
    email = str(input("Email: "))           
    senha = str(input("Senha: "))
    listaProduto = []    
    listaProdutoConvertida = json.dumps(listaProduto)
    conexaoCassandra.execute(
        '''INSERT INTO vendedor (email, documento, nome, senha, listaproduto) 
        VALUES (%s, %s, %s, %s, %s);''', 
        (email, documento, nome, senha, listaProdutoConvertida)
    )
    print(f'\nVendedor {nome} inserido com sucesso!\n')

def listarVendedor(conexaoCassandra):
    objetoVendedorEscolhido = consultaVendedor(conexaoCassandra)
    objetoVendedorProduto = json.loads(objetoVendedorEscolhido['listaproduto'])    
    print(f"Nome: {objetoVendedorEscolhido['nome']}")
    print(f"Documento: {objetoVendedorEscolhido['documento']}")
    print(f"Email: {objetoVendedorEscolhido['email']}")
    print(f"Senha: {objetoVendedorEscolhido['senha']}")
    print("\nProdutos:")
    for produto in objetoVendedorProduto:
        print(f"\nDescrição: {produto['descricao']}")
        print(f"Preço: R${produto['preco']}")
        print(f"Quantidade: {produto['quantidade']}")
        print("\n---------------------------------------\n")

def atualizarVendedor(conexaoCassandra):
    objetoVendedorEscolhido = consultaVendedor(conexaoCassandra)
    novoNome = str(input("Nome: "))
    novoEmail = str(input("Email: "))
    novaSenha = str(input("Senha: "))
    conexaoCassandra.execute(
        '''UPDATE vendedor
        SET email = %s, nome = %s, senha = %s 
        WHERE documento = %s;''', 
        (novoEmail, novoNome, novaSenha, objetoVendedorEscolhido['documento'])
    )
    print(f'\nVendedor {novoNome} atualizado com sucesso!\n')

def deletarVendedor(conexaoCassandra):
    objetoVendedorEscolhido = consultaVendedor(conexaoCassandra)
    conexaoCassandra.execute(
        "DELETE FROM vendedor WHERE documento = %s;",
        (objetoVendedorEscolhido['documento'],)
    )
    print(f"\nVendedor {objetoVendedorEscolhido['nome']} foi deletado com sucesso!\n")

def consultaVendedor(conexaoCassandra):
    while True:
        documento = str(input("Documento do vendedor: "))
        vendedorEscolhido = conexaoCassandra.execute("SELECT * FROM vendedor WHERE documento = %s;", (documento,))
        if not vendedorEscolhido:
            print("Nenhum vendedor encontrado")
        else:
            objetoVendedorEscolhido = vendedorEscolhido.one()._asdict()
            break
    return objetoVendedorEscolhido

def vinculaProdutoVendedor(descricao, preco, quantidadeProduto, conexaoCassandra):
    objetoVendedorEscolhido = consultaVendedor(conexaoCassandra)
    objetoListaProdutoVendedor = json.loads(objetoVendedorEscolhido['listaproduto'])
    produto = {
        "descricao": descricao,
        "preco": preco,
        "quantidade": quantidadeProduto
    }
    if produto in objetoListaProdutoVendedor:
        print("Esse vendedor já possui esse produto!")
        return True
    else:
        objetoListaProdutoVendedor.append(produto)
        jsonListaProdutoVendedor = json.dumps(objetoListaProdutoVendedor)
        conexaoCassandra.execute(
            "UPDATE vendedor SET listaproduto = %s WHERE documento = %s;", 
            (jsonListaProdutoVendedor, objetoVendedorEscolhido['documento'])
        )
        return [objetoVendedorEscolhido['nome'], objetoVendedorEscolhido['documento']]

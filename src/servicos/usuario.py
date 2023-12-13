import json


def criarUsuario(conexaoCassandra):
    nome = str(input("Nome: "))
    while True:
        cpf = str(input("CPF: "))
        usuarioEscolhido = conexaoCassandra.execute("SELECT * FROM usuario WHERE cpf = %s;", (cpf,))
        if not usuarioEscolhido:
            break
        else:
            print("Já exite um usuário cadastrado com esse CPF!")        
    email = str(input("Email: "))           
    senha = str(input("Senha: "))
    telefone = str(input("Número telefone: "))
    listaEndereco = []
    listaCompra = []
    listaFavorito = []
    key = "S"
    while key == "S":
        cep = str(input("CEP: "))
        ruaAvenida = str(input("Nome da rua ou avenida: "))
        numeroEndereco = str(input("Número endereço: "))
        bairro = str(input("Bairro: "))
        cidade = str(input("Cidade: "))
        estado = str(input("Estado(Sigla): "))
        endereco = {
            "cep": cep,
            "rua_avenida": ruaAvenida,
            "numero": numeroEndereco,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,            
            }
        listaEndereco.append(endereco)
        key = input("Deseja cadastrar um novo endereço(S/N)? ").upper()
    
    listaEnderecoConvertida = json.dumps(listaEndereco)
    listaCompraConvertida = json.dumps(listaCompra)
    listaFavoritoConvertida = json.dumps(listaFavorito)
    conexaoCassandra.execute(
        '''INSERT INTO usuario (email, cpf, listacompra, listaendereco, listafavorito, nome, senha, telefone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''', 
        (email, cpf, listaCompraConvertida, listaEnderecoConvertida, listaFavoritoConvertida, nome, senha, telefone))
    print(f'\nUsuário {nome} inserido com sucesso!\n')

def listarUsuario(conexaoCassandra):
    objetoUsuarioEscolhido = consultaUsuario(conexaoCassandra)
    objetoUsuarioEndereco = json.loads(objetoUsuarioEscolhido['listaendereco'])    
    print(f"Nome: {objetoUsuarioEscolhido['nome']}")
    print(f"Cpf: {objetoUsuarioEscolhido['cpf']}")
    print(f"Email: {objetoUsuarioEscolhido['email']}")
    print(f"Senha: {objetoUsuarioEscolhido['senha']}")
    print(f"Telefone: {objetoUsuarioEscolhido['telefone']}")
    print("\nEndereços:")
    for endereco in objetoUsuarioEndereco:
        print(f"Cep: {endereco['cep']}")
        print(f"Rua/Avenida: {endereco['rua_avenida']}")
        print(f"Número: {endereco['numero']}")
        print(f"Bairro: {endereco['bairro']}")
        print(f"Cidade: {endereco['cidade']}")
        print(f"Estado: {endereco['estado']}")
        print("\n---------------------------------------\n")

def atualizarUsuario(conexaoCassandra):
    objetoUsuarioEscolhido = consultaUsuario(conexaoCassandra)
    if not objetoUsuarioEscolhido:
        print("Nenhum usuário cadastrado com esse email!")
    else:
        novoNome = str(input("Nome: "))
        novoEmail = str(input("Email: "))
        novaSenha = str(input("Senha: "))
        novoTelefone = str(input("Número telefone: "))
        conexaoCassandra.execute(
            '''UPDATE usuario
            SET email = %s, nome = %s, senha = %s, telefone = %s 
            WHERE cpf = %s;''', 
            (novoEmail, novoNome, novaSenha, novoTelefone, objetoUsuarioEscolhido['cpf']))
            
        print(f'\nUsuário {novoNome} atualizado com sucesso!\n')

def criarEndereco(conexaoCassandra):
    objetoUsuarioEscolhido = consultaUsuario(conexaoCassandra)
    objetoListaEnderecoUsuario = json.loads(objetoUsuarioEscolhido['listaendereco'])
    cep = str(input("CEP: "))
    ruaAvenida = str(input("Nome da rua ou avenida: "))
    numeroEndereco = input(input("Número endereço: "))
    bairro = str(input("Bairro: "))
    cidade = str(input("Cidade: "))
    estado = str(input("Estado(Sigla): "))
    objetoNovoEndereco = {
        "cep": cep,
        "rua_avenida": ruaAvenida,
        "numero": numeroEndereco,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado, 
    }
    objetoListaEnderecoUsuario.append(objetoNovoEndereco)
    jsonListaEnderecoUsuario = json.dumps(objetoListaEnderecoUsuario)
    conexaoCassandra.execute(
            "UPDATE usuario SET listaendereco = %s WHERE cpf = %s;",
            (jsonListaEnderecoUsuario, objetoUsuarioEscolhido['cpf'])
            )
    print(f'\nEndereço cadastrado com sucesso!\n')

def deletarUsuario(conexaoCassandra):
    objetoUsuarioEscolhido = consultaUsuario(conexaoCassandra)
    conexaoCassandra.execute(
        "DELETE FROM usuario WHERE cpf = %s;",
        (objetoUsuarioEscolhido['cpf'],)
        )
    print(f"\nUsuário {objetoUsuarioEscolhido['nome']} foi deletado com sucesso!\n")

def vinculaCompraUsuario(listaProdutoCompra, data_entrega, data_compra, valorCompra, conexaoCassandra):
    usuarioEscolhido = consultaUsuario(conexaoCassandra)
    listaProduto = []
    for produto in listaProdutoCompra:
        objetoProduto = {
            "descricao": produto['descricao'],
            "preco": produto['preco'],
            "quantidade": produto['quantidadeProdutoCompra'],
            "vendedor": produto['vendedor']
        }
        listaProduto.append(objetoProduto)
    compra = {
        "listaProduto": listaProduto,
        "dataEntrega": data_entrega,
        "dataCompra": data_compra,
        "valorTotalCompra": valorCompra
    }
    listaCompraUsuario = json.loads(usuarioEscolhido['listacompra'])
    listaCompraUsuario.append(compra)
    jsonCompraUsuario = json.dumps(listaCompraUsuario)
    conexaoCassandra.execute(
            "UPDATE usuario SET listacompra = %s WHERE cpf = %s;",
            (jsonCompraUsuario, usuarioEscolhido['cpf'])
            )
    return [usuarioEscolhido["nome"], usuarioEscolhido["cpf"]]

def listarComprasUsuario(conexaoCassandra):
    objetoUsuarioEscolhido = consultaUsuario(conexaoCassandra)
    objetoUsuarioCompra = json.loads(objetoUsuarioEscolhido['listacompra'])
    print("\nProdutos\n")
    for compra in objetoUsuarioCompra:
        print(f"Data entrega: {compra['dataEntrega']}")
        print(f"Data da compra: {compra['dataCompra']}")
        print(f"Preço Total : R${compra['valorTotalCompra']}")
        for produto in compra['listaProduto']:
            print(f"Descrição: {produto['descricao']}")
            print(f"Quantidade: {produto['quantidade']}")
            print("\n---------------------------------------\n")

def consultaUsuario(conexaoCassandra):
    while True:
        cpf = str(input("CPF do usuário: "))
        usuarioEscolhido = conexaoCassandra.execute("SELECT * FROM usuario WHERE cpf = %s;", (cpf,))
        if not usuarioEscolhido:
            print("Nenhum usuário encontrado")
        else:
            objetoUsuarioEscolhido = usuarioEscolhido.one()._asdict()
            break
    return objetoUsuarioEscolhido


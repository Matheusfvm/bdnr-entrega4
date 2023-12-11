from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import servicos.usuario as usuario
import servicos.vendedor as vendedor
import servicos.produto as produto
import servicos.compras as compra


cloud_config= {
   'secure_connect_bundle': 'secure-connect-mercadolivre.zip'
   }
with open("mercadoLivre-token.json") as f:
    secrets = json.load(f)
    
CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
conexaoCassandra = cluster.connect("mercado_livre")

key = 0
sub = 0
while key != 'S':
    print("\n1 - Usuário")
    print("2 - Vendedor")
    print("3 - Produto")
    print("4 - Compra")
    key = input("\nDigite a opção desejada?(S para sair) ")

    if key == '1':
        print("\n-----------------")
        print("\nMenu do Usuário\n")
        print("1 - Criar Usuário")
        print("2 - Listar Usuário")
        print("3 - Atualizar Usuário")
        print("4 - Apagar Usuário")
        print("5 - Adicionar novo Endereço")
        print("6 - Listar Compras")
        sub = input("\nDigite a opção desejada? (V para voltar) ")

        if sub == "1":
            print("\n----INSERIR USUÁRIO----\n")
            usuario.criarUsuario(conexaoCassandra)
            
        elif sub == "2":
            print("\n----LISTAR USUÁRIO----\n")
            usuario.listarUsuario(conexaoCassandra)
        
        elif sub == "3":
            print("\n----ATUALIZAR USUÁRIO----\n")
            usuario.atualizarUsuario(conexaoCassandra)

        elif sub == "4":
            print("\n----DELETAR USUÁRIO----")
            usuario.deletarUsuario(conexaoCassandra)
        
        elif sub == "5":
            print("\n----ADICIONAR ENDEREÇO----\n")
            usuario.criarEndereco(conexaoCassandra)
        
        elif sub == "6":
            print("\n----LISTAR COMPRAS----\n")
            usuario.listarComprasUsuario(conexaoCassandra)
    
    elif key == '2':
        print("\n-----------------")
        print("\nMenu do Vendedor\n")
        print("1 - Criar Vendedor")
        print("2 - Listar Vendedor")
        print("3 - Atualizar Vendedor")
        print("4 - Apagar Vendedor")
        sub = input("\nDigite a opção desejada? (V para voltar) ")

        if sub == "1":
            print("\n----INSERIR VENDEDOR----\n")
            vendedor.criarVendedor(conexaoCassandra)
            
        elif sub == "2":
            print("\n----LISTAR VENDEDOR----\n")
            vendedor.listarVendedor(conexaoCassandra)
        
        elif sub == "3":
            print("\n----ATUALIZAR VENDEDOR----\n")
            vendedor.atualizarVendedor(conexaoCassandra)

        elif sub == "4":
            print("\n----DELETAR VENDEDOR----")
            vendedor.deletarVendedor(conexaoCassandra)

    elif key == '3':
        print("\n-----------------")
        print("\nMenu do Produto\n") 
        print("1 - Criar Produto")
        print("2 - Listar Produto")
        print("3 - Atualizar Produto")
        print("4 - Apagar Produto")
        sub = input("\nDigite a opção desejada? (V para voltar) ")

        if sub == "1":
            print("\n----INSERIR PRODUTO----\n")
            produto.criarProduto(conexaoCassandra)
            
        elif sub == "2":
            print("\n----LISTAR PRODUTO----\n")
            produto.listarProduto(conexaoCassandra)
        
        elif sub == "3":
            print("\n----ATUALIZAR PRODUTO----\n")
            produto.atualizarProduto(conexaoCassandra)

        elif sub == "4":
            print("\n----DELETAR PRODUTO----\n")
            produto.deletarProduto(conexaoCassandra)
        
    elif key == '4':
        print("\n-----------------")
        print("\nMenu da Compra\n")
        print("1 - Comprar um Produto")
        print("2 - Listar Compras")
        sub = input("\nDigite a opção desejada? (V para voltar) ")

        if sub == "1":
            print("\n----COMPRAR UM PRODUTO----\n")
            compra.criarCompra(conexaoCassandra)
        
        if sub == "2":
            print("\n----LISTAR COMPRAS----\n")
            compra.criarCompra(conexaoCassandra)
    elif key == "S":
        break
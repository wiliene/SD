from Proxy import Proxy

def main():
    hostname = 'localhost'
    port = 1234  

    try:
        proxy = Proxy(hostname, port)

        while True:
            print("\nEscolha uma opção:")
            print("1. Adicionar Tarefa")
            print("2. Editar Tarefa")
            print("3. Remover Tarefa")
            print("4. Listar Tarefas")
            print("5. Sair")
            opcao = input("Opção: ")

            if opcao == '1':
                titulo = input("Título: ")
                descricao = input("Descrição: ")
                data_vencimento = input("Data de Vencimento (YYYY-MM-DD): ")
                task = {'titulo': titulo, 'descricao': descricao, 'data_vencimento': data_vencimento}
                response = proxy.adicionar_tarefa(task)
                print(f"Tarefa criada com ID: {response}")

            elif opcao == '2':
                task_id = input("ID da Tarefa: ")
                titulo = input("Novo Título: ")
                descricao = input("Nova Descrição: ")
                data_vencimento = input("Nova Data de Vencimento (YYYY-MM-DD): ")
                task = {'titulo': titulo, 'descricao': descricao, 'data_vencimento': data_vencimento}
                response = proxy.editar_tarefa(task_id, task)
                print(f"Tarefa {task_id} editada com sucesso.")

            elif opcao == '3':
                task_id = input("ID da Tarefa: ")
                response = proxy.remover_tarefa(task_id)
                print(f"Tarefa {task_id} removida com sucesso.")

            elif opcao == '4':
                tarefas = proxy.listar_tarefas()
                print("Tarefas cadastradas:")
                for tarefa in tarefas:
                    print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Descrição: {tarefa['descricao']}, Data de Vencimento: {tarefa['data_vencimento']}")

            elif opcao == '5':
                break

            else:
                print("Opção inválida. Tente novamente.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        proxy.close()

if __name__ == "__main__":
    main()

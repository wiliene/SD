from Proxy import Proxy
import re
from datetime import datetime

def validar_data(data_str):
    try:
        # Verifica se a data está no formato YYYY-MM-DD
        datetime.strptime(data_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Data inválida: {data_str}. O formato correto é YYYY-MM-DD.")

def validar_id(task_id):
    if not task_id.isdigit():
        raise ValueError(f"ID inválido: {task_id}. O ID deve ser numérico.")

def id_existe(task_id, tarefas):
    # Verifica se o ID fornecido existe na lista de tarefas
    return any(tarefa['id'] == int(task_id) for tarefa in tarefas)

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

                # Verifica se a data é válida
                try:
                    validar_data(data_vencimento)
                except ValueError as e:
                    print(e)
                    continue

                task = {'titulo': titulo, 'descricao': descricao, 'data_vencimento': data_vencimento}
                response = proxy.InsertTask(task)
                print(f"Tarefa criada com ID: {response}")

            elif opcao == '2':
                task_id = input("ID da Tarefa: ")

                # Verifica se o ID é válido
                try:
                    validar_id(task_id)
                except ValueError as e:
                    print(e)
                    continue

                # Verifica se o ID existe
                tarefas = proxy.listar_tarefas()
                if not id_existe(task_id, tarefas):
                    print(f"Erro: Tarefa com ID {task_id} não encontrada.")
                    continue

                titulo = input("Novo Título: ")
                descricao = input("Nova Descrição: ")
                data_vencimento = input("Nova Data de Vencimento (YYYY-MM-DD): ")

                try:
                    validar_data(data_vencimento)
                except ValueError as e:
                    print(e)
                    continue

                task = {'titulo': titulo, 'descricao': descricao, 'data_vencimento': data_vencimento}
                response = proxy.GetTaskById(task_id, task)
                print(f"Tarefa {task_id} editada com sucesso.")

            elif opcao == '3':
                task_id = input("ID da Tarefa: ")

                # Verifica se o ID é válido
                try:
                    validar_id(task_id)
                except ValueError as e:
                    print(e)
                    continue

                # Verifica se o ID existe
                tarefas = proxy.listar_tarefas()
                if not id_existe(task_id, tarefas):
                    print(f"Erro: Tarefa com ID {task_id} não encontrada.")
                    continue

                response = proxy.RemoveTask(task_id)
                print(f"Tarefa {task_id} removida com sucesso.")

            elif opcao == '4':
                tarefas = proxy.GetAllTasks()
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
2

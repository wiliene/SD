from UDPClient import UDPClient

class Proxy:
    def __init__(self, hostname, port):
        self.client = UDPClient(hostname, port)

    def do_operation(self, action, **params):
        
        # Cria a requisição com a ação e parâmetros fornecidos
        request = {
            "action": action,
            **params  # Inclui quaisquer parâmetros adicionais na requisição
        }
        self.client.send_request(request)
        response = self.client.receive_response(request)
        print(f"Resposta recebida: {response}")
        return response

    def adicionar_tarefa(self, task):
        # adicionar uma tarefa
        response = self.do_operation("adicionar_tarefa", task=task)
        return response.get('taskId')  # Retorna o ID da tarefa criada

    def editar_tarefa(self, task_id, task):
        #  editar uma tarefa
        response = self.do_operation("editar_tarefa", task_id=task_id, task=task)
        return response

    def remover_tarefa(self, task_id):
        # remover uma tarefa
        response = self.do_operation("remover_tarefa", task_id=task_id)
        return response

    def listar_tarefas(self):
        # listar tarefas
        response = self.do_operation("listar_tarefas")
        return response.get('tarefas', [])  # Retorna uma lista de tarefas

    def close(self):
        self.client.close()

from UDPClient import UDPClient

class Proxy:
    def __init__(self, hostname, port):
        self.client = UDPClient(hostname, port)

    def adicionar_tarefa(self, task):
        request = {
            "action": "adicionar_tarefa",
            "task": task
        }
        self.client.send_request(request)
        # Corrigido: usa o método correto 'receive_response'
        response = self.client.receive_response(request)
        print(f"Resposta recebida: {response}")
        return response.get('taskId')  # Retorna o ID da tarefa criada

    def editar_tarefa(self, task_id, task):
        request = {
            "action": "editar_tarefa",
            "task_id": task_id,
            "task": task
        }
        self.client.send_request(request)
        # Corrigido: usa o método correto 'receive_response'
        response = self.client.receive_response(request)
        print(f"Resposta recebida: {response}")
        return response

    def remover_tarefa(self, task_id):
        request = {
            "action": "remover_tarefa",
            "task_id": task_id
        }
        self.client.send_request(request)
        # Corrigido: usa o método correto 'receive_response'
        response = self.client.receive_response(request)
        print(f"Resposta recebida: {response}")
        return response

    def listar_tarefas(self):
        request = {
            "action": "listar_tarefas"
        }
        self.client.send_request(request)
        # Corrigido: usa o método correto 'receive_response'
        response = self.client.receive_response(request)
        print(f"Resposta recebida: {response}")
        return response.get('tarefas', [])  # Retorna uma lista de tarefas

    def close(self):
        self.client.close()

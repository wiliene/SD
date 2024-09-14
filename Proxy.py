from UDPClient import UDPClient, RequestMessage  # Importe também a classe RequestMessage

class Proxy:
    def __init__(self, hostname, port):
        self.client = UDPClient(hostname, port)

    def do_operation(self, action, **params):
        # Cria o objeto mensagem (RequestMessage)
        request_message = RequestMessage(
            obj_reference="db",  # Supondo que o obj_reference seja "db"
            method_id=action,    # O método é o nome da ação
            args=params,         # Passa os parâmetros como argumento
            t=0,                 # Pode ajustar esse valor conforme a lógica do seu sistema
            id_value=1           # Exemplo: ID fixo, ou você pode gerar dinamicamente
        )
        
        # Envia a requisição
        self.client.send_request(request_message)
        
        # Recebe a resposta
        response = self.client.receive_response(request_message)
        print(f"Resposta recebida: {response}")
        return response

    def adicionar_tarefa(self, task):
        # Adicionar uma tarefa
        response = self.do_operation("adicionar_tarefa", task=task)
        return response.get('taskId')  # Retorna o ID da tarefa criada

    def editar_tarefa(self, task_id, task):
        # Editar uma tarefa
        response = self.do_operation("editar_tarefa", task_id=task_id, task=task)
        return response

    def remover_tarefa(self, task_id):
        # Remover uma tarefa
        response = self.do_operation("remover_tarefa", task_id=task_id)
        return response

    def listar_tarefas(self):
        # Listar tarefas
        response = self.do_operation("listar_tarefas")
        return response.get('tarefas', [])  # Retorna uma lista de tarefas

    def close(self):
        self.client.close()

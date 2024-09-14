import json
from UDPClient import UDPClient, RequestMessage

class Proxy:
    def __init__(self, hostname, port):
        self.client = UDPClient(hostname, port)

    def do_operation(self, action, **params):
        # Converte os parâmetros em JSON
        args_json = json.dumps(params)
        args_bytes = args_json.encode('utf-8')  # Codifica diretamente em bytes

        # Cria o objeto mensagem (RequestMessage)
        request_message = RequestMessage(
            obj_reference="db",
            method_id=action,
            args=args_bytes,  # Passa os parâmetros como bytes
            t=1,
            id_value=1
        )
        
        # Envia a requisição
        self.client.send_request(request_message)
        
        # Recebe a resposta
        response = self.client.receive_response(request_message)
        print(f"Resposta recebida: {response}")
        return response

    def InsertTask(self, task):
        # Adiciona uma tarefa
        response = self.do_operation("InsertTask", task=task)
        return response.get('taskId')  # Retorna o ID da tarefa criada

    def GetTaskById(self, task_id, task):
        # Edita uma tarefa
        response = self.do_operation("GetTaskById", task_id=task_id, task=task)
        return response

    def RemoveTask(self, task_id):
        # Remove uma tarefa
        response = self.do_operation("RemoveTask", task_id=task_id)
        return response

    def GetAllTasks(self):
        # Lista todas as tarefas
        response = self.do_operation("GetAllTasks")
        return response.get('tarefas', [])  # Retorna uma lista de tarefas

    def close(self):
        self.client.close()

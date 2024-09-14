from UDPClient import UDPClient, Message  # Importe a classe Message
import json
import base64
class Proxy:
    def __init__(self, hostname, port):
        self.client = UDPClient(hostname, port)

    def do_operation(self, action, **params):
        # Converte os parâmetros em JSON
        args_json = json.dumps(params)
        args_bytes = args_json.encode('utf-8')  # Codifica diretamente em bytes

        # Cria o objeto Message com os parâmetros convertidos em bytes
        request_message = Message(
            obj_reference="db",       # Supondo que o obj_reference seja "db"
            method_id=action,         # O método é o nome da ação
            request_bytes=args_bytes, # Passa os parâmetros como bytes
            t=1,                     # Pode ajustar esse valor conforme a lógica do seu sistema
            id_value=1               # Exemplo: ID fixo, ou você pode gerar dinamicamente
        )

        # Envia a requisição
        self.client.send_request(request_message.to_bytes())

        # Recebe a resposta
        response_bytes = self.client.receive_response()
        if response_bytes:
            # Desserializa a resposta JSON
            response_json = json.loads(response_bytes.decode('utf-8'))

            # Converte o campo base64 'Args' de volta para bytes
            args_base64 = response_json.get('Args', '')
            args_bytes = base64.b64decode(args_base64)

            # Desserializa os bytes para um dicionário Python
            response_data = json.loads(args_bytes.decode('utf-8'))
            
            print(f"Resposta recebida: {response_data}")
            return response_data

        print("Erro: Não foi possível receber a resposta do servidor.")
        return None

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

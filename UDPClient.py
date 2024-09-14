import socket
import json

# Define a classe Task para representar uma tarefa
class Task:
    def __init__(self, titulo, descricao, data):
        self.titulo = titulo
        self.descricao = descricao
        self.data = data

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data": self.data
        }

# Define a classe RequestMessage para representar uma mensagem de requisição
class RequestMessage:
    def __init__(self, obj_reference, method_id, args, t, id_value):
        self.ObjReference = obj_reference
        self.MethodID = method_id
        self.Args = args
        self.T = t
        self.ID = id_value
        self.StatusCode = 202

    def to_json(self):
        # Converte o objeto em um dicionário e depois em uma string JSON
        return json.dumps(self.__dict__)

class UDPClient:
    def __init__(self, hostname, port, timeout=5, max_retries=3):
        self.server_address = (hostname, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)  # Define o timeout para o socket
        self.max_retries = max_retries

    def send_request(self, request_message):
        # Converte a mensagem para JSON e depois para bytes
        json_request = request_message.to_json()
        byte_request = json_request.encode('utf-8')  # Converte para array de bytes

        # Envia a mensagem em formato de bytes para o servidor
        self.socket.sendto(byte_request, self.server_address)

    def receive_response(self, request_message):
        # Tenta receber uma resposta JSON do servidor via UDP, com tratamento de timeout e reenvio.
        retries = 0
        while retries < self.max_retries:
            try:
                packet, _ = self.socket.recvfrom(4096)
                json_response = packet.decode()  # Decodifica de volta para string
                return json.loads(json_response)  # Converte a string JSON de volta para objeto Python
            except socket.timeout:
                retries += 1
                print(f"Timeout! Tentativa {retries} de {self.max_retries}. Reenviando a mensagem...")
                self.send_request(request_message)  # Reenvia a mensagem

        print("Erro: Número máximo de tentativas alcançado. Falha na comunicação com o servidor.")
        return None  # Retorna None se o número máximo de tentativas for alcançado

    def close(self):
        # Fecha o socket UDP.
        self.socket.close()



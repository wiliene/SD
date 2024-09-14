import socket
import json

# Define a classe RequestMessage para representar uma mensagem de requisição
class RequestMessage:
    def __init__(self, obj_reference, method_id, args, t, id_value):
        self.ObjReference = obj_reference
        self.MethodID = method_id
        self.Args = args
        self.T = t
        self.ID = id_value
        self.StatusCode = 0

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
        # Envia a mensagem JSON para o servidor via UDP.
        json_request = request_message.to_json()  # Usa o método da classe para converter a mensagem para JSON
        self.socket.sendto(json_request.encode(), self.server_address)

    def receive_response(self, request_message):
        # Tenta receber uma resposta JSON do servidor via UDP, com tratamento de timeout e reenvio.
        retries = 0
        while retries < self.max_retries:
            try:
                packet, _ = self.socket.recvfrom(4096)
                json_response = packet.decode()
                return json.loads(json_response)
            except socket.timeout:
                retries += 1
                print(f"Timeout! Tentativa {retries} de {self.max_retries}. Reenviando a mensagem...")
                self.send_request(request_message)  # Reenvia a mensagem

        print("Erro: Número máximo de tentativas alcançado. Falha na comunicação com o servidor.")
        return None  # Retorna None se o número máximo de tentativas for alcançado

    def close(self):
        # Fecha o socket UDP.
        self.socket.close()


if __name__ == "__main__":
    client = UDPClient('localhost', 12345)

    # Exemplo de criação e envio de uma requisição 'Insert'
    task = {
        "id": 1,
        "name": "Exemplo de Tarefa",
        "description": "Essa é uma tarefa de exemplo"
    }

    # Cria uma instância de RequestMessage em vez de usar uma função
    request_message = RequestMessage("db", "Insert", task, 201, 9223372036854775806)
    
    # Envia a requisição
    client.send_request(request_message)

    # Recebe a resposta do servidor
    response = client.receive_response(request_message)
    if response:
        print("Resposta do Servidor:", response)

    # Fecha o cliente
    client.close()

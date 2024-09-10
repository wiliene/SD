import socket
import json

class UDPClient:
    def __init__(self, hostname, port, timeout=5, max_retries=3):
        self.server_address = (hostname, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)  # Define o timeout para o socket
        self.max_retries = max_retries

    def create_request(self, obj_reference, method_id, args, t, id_value):
       
        return {
            "ObjReference": obj_reference,
            "MethodID": method_id,
            "Args": args,
            "T": t,
            "ID": id_value,
            "StatusCode": 0
        }

    def send_request(self, request):
        
        #Envia uma requisição JSON para o servidor via UDP.
        
        json_request = json.dumps(request)
        self.socket.sendto(json_request.encode(), self.server_address)

    def receive_response(self, request):
        
        #Tenta receber uma resposta JSON do servidor via UDP, com tratamento de timeout e reenvio.
        
        retries = 0
        while retries < self.max_retries:
            try:
                packet, _ = self.socket.recvfrom(4096)
                json_response = packet.decode()
                return json.loads(json_response)
            except socket.timeout:
                retries += 1
                print(f"Timeout! Tentativa {retries} de {self.max_retries}. Reenviando a mensagem...")
                self.send_request(request)  # Reenvia a mensagem

        print("Erro: Número máximo de tentativas alcançado. Falha na comunicação com o servidor.")
        return None  # Retorna None se o número máximo de tentativas for alcançado

    def close(self):
        """
        Fecha o socket UDP.
        """
        self.socket.close()


if __name__ == "__main__":
    client = UDPClient('localhost', 12345)

    # Exemplo de criação e envio de uma requisição 'Insert'
    task = {
        "id": 1,
        "name": "Exemplo de Tarefa",
        "description": "Essa é uma tarefa de exemplo"
    }

    request = client.create_request("db", "Insert", task, 201, 9223372036854775806)
    client.send_request(request)

    
    response = client.receive_response(request)
    if response:
        print("Resposta do Servidor:", response)

    # Fecha o cliente
    client.close()

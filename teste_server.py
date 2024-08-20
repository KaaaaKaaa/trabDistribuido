# Arquivo de teste do server
import Pyro5.api
import time

def teste_server():
   # toda vez eu tenho que substituir pelo que ta rodando agora :\
    server_uri = "PYRO:obj_37012648769f44bb91a1540124b33efa@localhost:51482"
    server = Pyro5.api.Proxy(server_uri)
    
    # Teste upload de arquivo FUNCIONA :)
    file_content = "Conteúdo do arquivo".encode('utf-8')
    print("Testando upload de arquivo...")
    print(server.upload_file("example.txt", file_content))
    
    # Teste listagem de arquivos FUNCIONA :)
    print("Listando arquivos disponíveis...")
    print(server.list_files())
    
    # Teste download de arquivo FUNCIONA :)
    print("Testando download de arquivo...")
    print("Conteúdo do arquivo baixado:", server.download_file("example.txt"))
    
    # Teste  registro de interesse NAO FUNCIONA :(
    print("Registrando interesse em um arquivo...")
    # Pra registrar interesse, precisa de um cliente, então eu usei uma instancia simples de FileClient
    class DummyFileClient:
        def notify_event(self, message):
            print(f"Notificação recebida: {message}")
    
    dummy_client = DummyFileClient()
    print(server.register_interest("not_yet_uploaded.txt", dummy_client, 300)) 
    
    # Simulação da adição do arquivo e o tempo passando
    time.sleep(2)
    
    # Teste cancelamento de interesse NAO FUNCIONA:(
    print("Cancelando interesse em um arquivo...")
    print(server.cancel_interest("not_yet_uploaded.txt", dummy_client))

if __name__ == "__main__":
    teste_server()

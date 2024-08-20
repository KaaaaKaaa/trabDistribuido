import Pyro5.api
import base64
import time

# Classe do cliente que vai se conectar com o servidor Pyro
@Pyro5.api.expose
class FileClient:
    def __init__(self, server_uri):
        # Guardando a referência do servidor no cliente
        self.server = Pyro5.api.Proxy(server_uri)

    # Método para enviar arquivos pro servidor
    def upload_file(self, filename, filedata):
        # Codificando o arquivo em base64 (pra ficar tudo no formato de string)
        encoded_data = base64.b64encode(filedata).decode('utf-8')
        # Enviando o arquivo pro servidor com a codificação informada
        return self.server.upload_file(filename, {'data': encoded_data, 'encoding': 'base64'})

    # Método pra listar os arquivos disponíveis no servidor
    def list_files(self):
        return self.server.list_files()

    # Método pra baixar um arquivo do servidor
    def download_file(self, filename):
        # Recebendo o arquivo do servidor
        filedata = self.server.download_file(filename)
        # Decodificando o arquivo se vier em base64
        if isinstance(filedata, dict):
            decoded_data = base64.b64decode(filedata['data'])
            return decoded_data
        return filedata

    # Método pra pegar o conteúdo de um arquivo no servidor
    def get_file_content(self, filename):
        return self.server.get_file_content(filename)

    # Método pra registrar interesse em um arquivo específico, pra ser notificado quando ele for enviado
    def register_interest(self, filename, duration):
        return self.server.register_interest(filename, self, duration)

    # Método pra cancelar o interesse em um arquivo
    def cancel_interest(self, filename):
        return self.server.cancel_interest(filename, self)

    # Método que vai ser chamado quando o servidor notificar algum evento
    def notify_event(self, message):
        print(f"Notificação recebida: {message}")

# Função pra criar alguns arquivos de exemplo no sistema
def create_example_files():
    example_files = {
        "file1.txt": "Este é o conteúdo do arquivo 1.",
        "file2.txt": "Este é o conteúdo do arquivo 2.",
        "file3.txt": "Este é o conteúdo do arquivo 3.",
    }
    for filename, content in example_files.items():
        with open(filename, "w") as file:
            file.write(content)

# Função de teste pra ver se o cliente tá funcionando certinho 
# TEM QUE MUDAR TODA VEZ ESSA BUDEGA
def test_client_functions():
    server_uri = "PYRO:obj_37012648769f44bb91a1540124b33efa@localhost:51482"
    client = FileClient(server_uri)

    # Criando os arquivos de exemplo
    create_example_files()

    # Enviando os arquivos de exemplo pro servidor
    for filename in ["file1.txt", "file2.txt", "file3.txt"]:
        with open(filename, "rb") as file:
            file_content = file.read()
            print(f"Enviando {filename}:")
            print(client.upload_file(filename, file_content))

    # Listando os arquivos disponíveis no servidor
    print("Arquivos disponíveis:")
    print(client.list_files())

    # Baixando os arquivos do servidor e mostrando o conteúdo
    for filename in ["file1.txt", "file2.txt", "file3.txt"]:
        print(f"Conteúdo do arquivo baixado ({filename}):")
        downloaded_content = client.download_file(filename)
        print(downloaded_content.decode('utf-8'))

    # Verificando o conteúdo direto no servidor DAQUI PRA BAIXO NAO FUNCIONA :(
    for filename in ["file1.txt", "file2.txt", "file3.txt"]:
        print(f"Conteúdo do arquivo no servidor ({filename}):")
        server_content = client.get_file_content(filename)
        print(server_content)

    # Registrando interesse em um arquivo que ainda não foi enviado
    print("Registrando interesse por 'file4.txt' que ainda não foi enviado:")
    print(client.register_interest("file4.txt", 300))  # 300 segundos

    # Enviando o arquivo de interesse (file4.txt) pro servidor
    print("Enviando 'file4.txt':")
    with open("file4.txt", "w") as file:
        file.write("Este é o conteúdo do arquivo 4.")
    with open("file4.txt", "rb") as file:
        file_content = file.read()
        print(client.upload_file("file4.txt", file_content))

    # Dando uma pausa pra garantir que a notificação seja recebida 
    print("Aguardando notificação...")
    time.sleep(5)

    # Cancelando o interesse pelo arquivo (file4.txt)
    print("Cancelando interesse por 'file4.txt':")
    print(client.cancel_interest("file4.txt"))

    # Limpeza: deletando os arquivos de exemplo
    import os
    for filename in ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]:
        if os.path.exists(filename):
            os.remove(filename)

# Ponto de entrada do script
if __name__ == "__main__":
    test_client_functions()

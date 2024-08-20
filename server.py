import Pyro5.api

@Pyro5.api.expose
class FileServer:
    def __init__(self):
        self.files = {}  # dicionário para armazenar arquivos
        self.interests = {}  # dicionário para armazenar interesses dos clientes

    def upload_file(self, filename, filedata):
        self.files[filename] = filedata
        self.notify_clients(filename)
        return f"Arquivo {filename} enviado com sucesso!"

    def list_files(self):
        return list(self.files.keys())

    def download_file(self, filename):
        return self.files.get(filename, "Arquivo não encontrado.")

    def register_interest(self, filename, client, duration):
        self.interests[filename] = (client, duration)
        return f"Interesse registrado para o arquivo {filename}."

    def cancel_interest(self, filename, client):
        if filename in self.interests and self.interests[filename][0] == client:
            del self.interests[filename]
            return f"Interesse para o arquivo {filename} cancelado."
        return "Interesse não encontrado ou não corresponde ao cliente."

    def notify_clients(self, filename):
        if filename in self.interests:
            client, duration = self.interests[filename]
            client.notify_event(f"O arquivo {filename} agora está disponível.")
            del self.interests[filename]

# Iniciar o servidor
daemon = Pyro5.server.Daemon()  # cria um daemon Pyro
uri = daemon.register(FileServer)  # registra a classe no Pyro
print(f"URI do servidor: {uri}")

daemon.requestLoop()  # inicia o loop de requisições do servidor

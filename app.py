import uvicorn
from src.config.login.index import *
from src.config.email.verificar.verificarmail import *
from src.config.email.recuperar_senha.index import *
from src.routes.funcionarios_rotas.clientes.routes import *
from src.routes.funcionarios_rotas.funcionarios.routes import *
from src.routes.clientes_rotas.clientes.routes import *
from src.routes.clientes_rotas.enderecos.routes import *
from src.routes.funcionarios_rotas.categorias.routes import *
from src.routes.funcionarios_rotas.produtos.routes import *
from src.routes.funcionarios_rotas.produtos_in_estoque.routes import *
from src.routes.clientes_rotas.categorias.routes import *
from src.routes.clientes_rotas.produto.routes import *

if __name__ == "__main__":
    uvicorn.run("src.configure:app", port=5000, reload=True)
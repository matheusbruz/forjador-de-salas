# Forjador de Salas

## Visão Geral

Forjador de Salas é um bot para Discord desenvolvido em Python que automatiza a criação e gerenciamento de canais temporários personalizados. O bot utiliza um sistema "Join to Create" onde os usuários podem criar seus próprios espaços temporários simplesmente entrando em um canal designado.

## Funcionalidades

- **Sistema "Join to Create"**: Configuração de um canal específico que, quando acessado, cria automaticamente uma sala personalizada para o usuário
- **Criação Automática de Salas**: Geração de uma categoria com canais de voz e texto personalizados
- **Prevenção de Duplicação**: Sistema inteligente que identifica se o usuário já possui uma sala, evitando criações desnecessárias
- **Movimentação Automática**: Transporte imediato do usuário para sua sala recém-criada
- **Gerenciamento de Atividade**: Monitoramento da atividade dos usuários nos canais
- **Limpeza Automática**: Remoção de salas inativas após um período configurável (padrão: dois dias)

## Requisitos

- Python 3.8+
- discord.py 2.0.0+
- python-dotenv 0.19.0+ (opcional)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/forjador-de-salas.git
cd forjador-de-salas

# Instale as dependências
pip install -r requirements.txt
```

## Configuração

### Token do Bot

Configure o token do bot Discord utilizando um dos três métodos disponíveis:

1. **Arquivo config.json**:
   ```json
   {
     "token": "SEU_TOKEN_AQUI"
   }
   ```

2. **Arquivo .env**:
   ```
   DISCORD_TOKEN=SEU_TOKEN_AQUI
   ```

3. **Arquivo token.txt**:
   ```
   SEU_TOKEN_AQUI
   ```

### Permissões do Bot

O bot requer as seguintes permissões no Discord:
- Gerenciar Canais
- Gerenciar Mensagens
- Mover Membros
- Ver Canais
- Enviar Mensagens

### Adição ao Servidor

1. Acesse o [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications)
2. Selecione sua aplicação
3. Navegue até a seção OAuth2
4. Selecione os escopos `bot` e `applications.commands`
5. Selecione as permissões necessárias
6. Utilize o URL gerado para adicionar o bot ao seu servidor

## Uso

### Inicialização

```bash
python main.py
```

### Comandos Disponíveis

| Comando | Descrição | Permissão Necessária |
|---------|-----------|----------------------|
| `!setjoinchannel [canal]` | Define o canal "join to create" | Administrador |

Se nenhum canal for especificado no comando `!setjoinchannel`, o bot utilizará o canal de voz atual do usuário.

### Processo de Funcionamento

1. **Configuração Inicial**: Um administrador define o canal "join to create" através do comando `!setjoinchannel`
2. **Criação de Salas**: Quando um usuário entra no canal designado, o sistema:
   - Cria uma categoria chamada "Mesa de @usuario"
   - Cria um canal de voz chamado "Mesa de @usuario"
   - Cria um canal de texto chamado "Rolagem de @usuario"
   - Move o usuário para o canal de voz criado
3. **Prevenção de Duplicação**: Se o usuário já possuir uma sala, será redirecionado para ela em vez de criar uma nova
4. **Gestão de Inatividade**: O sistema monitora a atividade do usuário criador e remove a sala após dois dias de inatividade

## Estrutura do Projeto

```
forjador-de-salas/
├── main.py               # Arquivo principal e inicialização do bot
├── config.py             # Gerenciamento de configurações
├── channels_manager.py   # Gerenciamento de canais temporários
├── config.json           # Arquivo de configuração (criado automaticamente)
├── .env                  # Arquivo de variáveis de ambiente (opcional)
├── token.txt             # Arquivo de token simplificado (opcional)
└── requirements.txt      # Dependências do projeto
```

## Customização

### Período de Inatividade

Para modificar o período máximo de inatividade antes da remoção automática, edite a seguinte linha no arquivo `channels_manager.py`:

```python
# Tempo máximo de inatividade (2 dias em segundos)
self.max_inactive_time = 2 * 24 * 60 * 60
```

### Nomenclatura dos Canais

A nomenclatura dos canais pode ser customizada editando as linhas correspondentes no método `_create_temp_channels` no arquivo `channels_manager.py`:

```python
# Criando um tópico (categoria) para os canais
category = await guild.create_category(f"Mesa de {member.display_name}")

# Criando canal de voz
voice_channel = await category.create_voice_channel(
    f"Mesa de {member.display_name}",
    overwrites=overwrites
)

# Criando canal de texto
text_channel = await category.create_text_channel(
    f"Rolagem de {member.display_name}",
    overwrites=overwrites
)
```

## Resolução de Problemas

### Erro "Token não encontrado"

- Verifique se o arquivo de configuração do token existe e está no formato correto
- Certifique-se de que o arquivo esteja no mesmo diretório do `main.py`
- Valide se o token está correto e ativo no [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications)

### Problemas de Permissão

- Verifique se o bot possui todas as permissões necessárias no servidor
- Certifique-se de que a hierarquia de cargos permite que o bot crie e modifique canais

## Desenvolvimento

### Arquivos Principais

- **main.py**: Inicialização do bot, registro de eventos e comandos
- **config.py**: Gerenciamento de configurações persistentes
- **channels_manager.py**: Lógica de criação e gerenciamento de canais temporários

### Contribuições

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um novo Pull Request

## Segurança

Este bot foi projetado para uso em servidores Discord onde existe confiança entre os membros. Para servidores públicos, recomenda-se implementar medidas adicionais de segurança.

## Contato

[Bruzaca](mailto:bruzacap@gmail.com)

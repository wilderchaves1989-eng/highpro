# HIGH PRO - Configuração MongoDB

## Pré-requisitos

- Python 3.8+
- pip (Python package manager)
- Conta MongoDB Atlas ativa

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

1. Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` com suas credenciais MongoDB:

```
MONGODB_URI=mongodb+srv://seu_usuario:sua_senha@seu_cluster.mongodb.net/high-pro?retryWrites=true&w=majority
MONGODB_DB=high-pro
MONGODB_COLAB_COLLECTION=colaboradores
MONGODB_HORAS_COLLECTION=horas
```

### 3. Obter a string de conexão MongoDB

1. Aceda ao [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Clique em **Connect** no seu cluster
3. Selecione **Connect your application**
4. Escolha **Python** como driver
5. Copie a string de conexão e substitua o `<password>` pela sua senha

## Uso

### Sincronizar dados do MongoDB

```bash
python sync_mongodb.py
```

Isto irá:
- ✅ Conectar ao MongoDB Atlas
- ✅ Buscar todos os colaboradores
- ✅ Buscar todos os registos de horas
- ✅ Exportar para `dados.json` (local)
- ✅ Sincronizar para `public/dados.json` (Vercel)

### Automatizar sincronização

#### Windows (Task Scheduler)

1. Abra **Task Scheduler**
2. Crie uma nova tarefa
3. Ação: Execute `python` com argumento `sync_mongodb.py`
4. Agendamento: Diário ou conforme necessário

#### macOS/Linux (Cron)

```bash
# Adicione ao crontab
crontab -e

# Sincronizar a cada hora
0 * * * * cd /caminho/para/high-pro && python sync_mongodb.py
```

## Resolução de Problemas

### "MONGODB_URI não configurada"
- Certifique-se de que o arquivo `.env` existe e tem a variável `MONGODB_URI`

### "Erro ao conectar ao MongoDB"
- Verifique se o cluster MongoDB Atlas está ativo
- Adicione seu IP à whitelist do MongoDB Atlas (Network Access)
- Confirme que a string de conexão está correta

### "Connection timeout"
- Verifique sua conexão de internet
- Tente novamente em alguns momentos
- Verifi...que se o MongoDB Atlas está disponível

## Deploy no Vercel

Após sincronizar os dados:

```bash
git add public/dados.json
git commit -m "Sync: atualizar dados do MongoDB"
git push origin main
```

Vercel irá fazer deploy automático com os dados atualizados.

## Estrutura dos dados

### colaboradores
```json
{
  "id": "uuid",
  "nome": "Nome Completo",
  "cargo": "Cargo",
  "email": "email@example.com",
  "telefone": "919001234",
  "tipoContrato": "fixo",
  "vencimento": 1500,
  "status": "ativo",
  "ativo": true,
  "arquivado": false,
  "cor": "#0564FF"
}
```

### horas
```json
{
  "colab_id": [
    {
      "data": "2026-07-06",
      "tipo": "horas",
      "qtd": 8,
      "obs": "Trabalho normal"
    }
  ]
}
```

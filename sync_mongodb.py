#!/usr/bin/env python3
"""
HIGH PRO - MongoDB Data Sync Script
Sincroniza dados do MongoDB com JSON local para a aplicação
"""

import json
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

class MongoDBSync:
    def __init__(self):
        self.uri = os.getenv('MONGODB_URI')
        self.db_name = os.getenv('MONGODB_DB', 'high-pro')
        self.colab_collection = os.getenv('MONGODB_COLAB_COLLECTION', 'colaboradores')
        self.horas_collection = os.getenv('MONGODB_HORAS_COLLECTION', 'horas')
        self.client = None
        self.db = None

    def connect(self):
        """Conectar ao MongoDB"""
        try:
            if not self.uri:
                print("❌ MONGODB_URI não configurada no arquivo .env")
                print("   Copie o arquivo .env.example para .env e configure as credenciais")
                return False

            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Testar conexão
            self.client.server_info()
            self.db = self.client[self.db_name]
            print("✅ Conectado ao MongoDB com sucesso!")
            return True
        except ConnectionFailure as e:
            print(f"❌ Erro ao conectar ao MongoDB: {e}")
            print("   Verifique:")
            print("   1. A string de conexão em MONGODB_URI")
            print("   2. Se o MongoDB Atlas está ativo")
            print("   3. Se o IP está na whitelist do MongoDB Atlas")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return False

    def fetch_colaboradores(self):
        """Buscar colaboradores do MongoDB"""
        try:
            collection = self.db[self.colab_collection]
            colabs = list(collection.find({}, {'_id': 0}))
            print(f"✅ {len(colabs)} colaboradores carregados")
            return colabs
        except Exception as e:
            print(f"❌ Erro ao buscar colaboradores: {e}")
            return []

    def fetch_horas(self):
        """Buscar horas do MongoDB"""
        try:
            collection = self.db[self.horas_collection]
            docs = list(collection.find({}, {'_id': 0}))
            horas = {}

            # Estruturar dados por colaborador
            for doc in docs:
                for colab_id, registos in doc.items():
                    if colab_id != '_id':
                        horas[colab_id] = registos if isinstance(registos, list) else []

            print(f"✅ Dados de horas carregados para {len(horas)} colaboradores")
            return horas
        except Exception as e:
            print(f"❌ Erro ao buscar horas: {e}")
            return {}

    def export_json(self, filename='dados.json'):
        """Exportar dados para JSON"""
        try:
            colabs = self.fetch_colaboradores()
            horas = self.fetch_horas()

            data = {
                'colaboradores': colabs,
                'horas': horas,
                'updated_at': datetime.now().isoformat()
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)

            print(f"✅ Dados exportados para {filename}")
            print(f"   Colaboradores: {len(colabs)}")
            print(f"   Registos de horas: {sum(len(h) for h in horas.values())}")
            return True
        except Exception as e:
            print(f"❌ Erro ao exportar JSON: {e}")
            return False

    def sync_to_vercel(self):
        """Exportar para pasta public (para Vercel)"""
        try:
            colabs = self.fetch_colaboradores()
            horas = self.fetch_horas()

            data = {
                'colaboradores': colabs,
                'horas': horas
            }

            public_path = 'public/dados.json'
            with open(public_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, default=str)

            print(f"✅ Dados sincronizados para {public_path}")
            return True
        except Exception as e:
            print(f"❌ Erro ao sincronizar para Vercel: {e}")
            return False

    def close(self):
        """Fechar conexão"""
        if self.client:
            self.client.close()
            print("✅ Conexão fechada")

def main():
    print("=" * 60)
    print("HIGH PRO - MongoDB Data Sync")
    print("=" * 60)
    print()

    sync = MongoDBSync()

    # Conectar
    if not sync.connect():
        print("\n⚠️  Não foi possível conectar ao MongoDB")
        print("   Por favor, configure o arquivo .env com as credenciais corretas")
        return

    print()

    # Sincronizar para JSON local
    sync.export_json()

    print()

    # Sincronizar para public (Vercel)
    sync.sync_to_vercel()

    print()

    # Fechar conexão
    sync.close()

    print()
    print("=" * 60)
    print("✅ Sincronização concluída com sucesso!")
    print("=" * 60)

if __name__ == '__main__':
    main()

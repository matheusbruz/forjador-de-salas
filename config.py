import json
import os
from pathlib import Path

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()
        
        # Garante que as estruturas básicas existam
        if 'guilds' not in self.config:
            self.config['guilds'] = {}
        if 'temp_channels' not in self.config:
            self.config['temp_channels'] = {}
            
        self._save_config()
    
    def _load_config(self):
        """Carrega as configurações do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"Arquivo de configuração {self.config_file} não encontrado. Criando um novo.")
                return {}
        except json.JSONDecodeError:
            print(f"Erro ao ler o arquivo de configuração {self.config_file}. Formato JSON inválido.")
            return {}
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return {}
    
    def _save_config(self):
        """Salva as configurações no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def get_token(self):
        """Retorna o token do bot"""
        token = self.config.get('token', '')
        if not token:
            print("Token não encontrado no arquivo de configuração.")
        return token
    
    def set_token(self, token):
        """Define o token do bot"""
        self.config['token'] = token
        self._save_config()
    
    def set_join_channel(self, guild_id, channel_id):
        """Define o canal 'join to create' para um servidor"""
        guild_id = str(guild_id)
        if guild_id not in self.config['guilds']:
            self.config['guilds'][guild_id] = {}
        
        self.config['guilds'][guild_id]['join_channel'] = channel_id
        self._save_config()
    
    def get_join_channel(self, guild_id):
        """Retorna o ID do canal 'join to create' de um servidor"""
        guild_id = str(guild_id)
        if guild_id in self.config['guilds']:
            return self.config['guilds'][guild_id].get('join_channel')
        return None
    
    def add_temp_channel(self, guild_id, user_id, category_id, voice_id, text_id):
        """Adiciona um canal temporário à configuração"""
        guild_id = str(guild_id)
        user_id = str(user_id)
        
        if guild_id not in self.config['temp_channels']:
            self.config['temp_channels'][guild_id] = {}
        
        self.config['temp_channels'][guild_id][user_id] = {
            'category_id': category_id,
            'voice_channel': voice_id,
            'text_channel': text_id,
            'last_activity': self._get_current_timestamp()
        }
        self._save_config()
    
    def update_channel_activity(self, guild_id, user_id):
        """Atualiza o timestamp de atividade de um canal temporário"""
        guild_id = str(guild_id)
        user_id = str(user_id)
        
        if (guild_id in self.config['temp_channels'] and 
            user_id in self.config['temp_channels'][guild_id]):
            self.config['temp_channels'][guild_id][user_id]['last_activity'] = self._get_current_timestamp()
            self._save_config()
    
    def remove_temp_channel(self, guild_id, user_id):
        """Remove um canal temporário da configuração"""
        guild_id = str(guild_id)
        user_id = str(user_id)
        
        if (guild_id in self.config['temp_channels'] and 
            user_id in self.config['temp_channels'][guild_id]):
            del self.config['temp_channels'][guild_id][user_id]
            self._save_config()
    
    def get_user_channels(self, guild_id, user_id):
        """Obtém os canais temporários de um usuário"""
        guild_id = str(guild_id)
        user_id = str(user_id)
        
        if (guild_id in self.config['temp_channels'] and 
            user_id in self.config['temp_channels'][guild_id]):
            return self.config['temp_channels'][guild_id][user_id]
        return None
    
    def get_all_temp_channels(self):
        """Retorna todos os canais temporários"""
        return self.config['temp_channels']
    
    def _get_current_timestamp(self):
        """Obtém o timestamp atual em formato string ISO"""
        import datetime
        return datetime.datetime.now().isoformat()
import discord
import datetime
import asyncio

class ChannelsManager:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        # Tempo máximo de inatividade (2 dias em segundos)
        self.max_inactive_time = 2 * 24 * 60 * 60
    
    async def handle_voice_state_update(self, member, before, after):
        """Gerencia a entrada/saída de usuários nos canais de voz"""
        # Ignora bots
        if member.bot:
            return
        
        # Verifica se o usuário entrou no canal "join to create"
        if after and after.channel:
            join_channel_id = self.config.get_join_channel(member.guild.id)
            
            if join_channel_id and after.channel.id == join_channel_id:
                # Verifica se o usuário já tem uma sala temporária
                existing_channels = self.config.get_user_channels(member.guild.id, member.id)
                
                if existing_channels:
                    # Se o usuário já tem sala, move-o para sua sala existente
                    voice_channel = member.guild.get_channel(existing_channels['voice_channel'])
                    if voice_channel:
                        await member.move_to(voice_channel)
                        # Atualiza o timestamp de atividade
                        self.config.update_channel_activity(member.guild.id, member.id)
                else:
                    # Cria nova sala para o usuário
                    await self._create_temp_channels(member)
        
        # Atualiza atividade se entrou no próprio canal temporário
        if after and after.channel:
            user_channels = self.config.get_user_channels(member.guild.id, member.id)
            if user_channels and user_channels['voice_channel'] == after.channel.id:
                self.config.update_channel_activity(member.guild.id, member.id)
    
    async def _create_temp_channels(self, member):
        """Cria canais temporários para o usuário"""
        guild = member.guild
        
        # Criando um tópico (categoria) para os canais
        category = await guild.create_category(f"Mesa de {member.display_name}")
        
        # Configura permissões
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=True),
            member: discord.PermissionOverwrite(manage_channels=True, manage_messages=True)
        }
        
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
        
        # Registra os canais temporários
        self.config.add_temp_channel(
            guild.id, 
            member.id, 
            category.id, 
            voice_channel.id, 
            text_channel.id
        )
        
        # Move o usuário para o canal de voz criado
        await member.move_to(voice_channel)
        
        # Envia mensagem de boas-vindas
        await text_channel.send(f"Bem-vindo à sua mesa, {member.mention}!")
    
    async def update_text_activity(self, message):
        """Atualiza a atividade quando o usuário envia mensagem no canal de texto"""
        guild_id = message.guild.id
        user_id = message.author.id
        
        user_channels = self.config.get_user_channels(guild_id, user_id)
        if user_channels and user_channels['text_channel'] == message.channel.id:
            self.config.update_channel_activity(guild_id, user_id)
    
    async def check_and_delete_inactive_channels(self):
        """Verifica e deleta canais inativos"""
        current_time = datetime.datetime.now()
        temp_channels = self.config.get_all_temp_channels()
        
        for guild_id, users in temp_channels.items():
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
                
            for user_id, channels_info in list(users.items()):
                # Converte o timestamp para objeto datetime
                last_activity = datetime.datetime.fromisoformat(channels_info['last_activity'])
                
                # Calcula o tempo de inatividade
                delta = current_time - last_activity
                
                # Se inativo por mais de 2 dias
                if delta.total_seconds() > self.max_inactive_time:
                    await self._delete_temp_channels(guild, user_id, channels_info)
    
    async def _delete_temp_channels(self, guild, user_id, channels_info):
        """Deleta os canais temporários de um usuário"""
        # Obter os objetos dos canais
        category = guild.get_channel(int(channels_info['category_id']))
        voice_channel = guild.get_channel(int(channels_info['voice_channel']))
        text_channel = guild.get_channel(int(channels_info['text_channel']))
        
        # Deleta os canais
        try:
            if text_channel:
                await text_channel.delete()
            if voice_channel:
                await voice_channel.delete()
            if category:
                await category.delete()
                
            # Remove do registro
            self.config.remove_temp_channel(guild.id, user_id)
            
            print(f"Canais temporários do usuário {user_id} foram removidos por inatividade.")
        except Exception as e:
            print(f"Erro ao deletar canais temporários: {e}")
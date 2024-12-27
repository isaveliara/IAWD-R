ERROR_MESSAGES = {
    "missing_params": "fromChannel and serverId are required.",
    "channel_or_server_registered": "The channel or server is already registered.",
    "invalid_server": "Invalid or unauthorized server ID.",
    "missing_channel": "fromChannel parameter is required.",
    "channel_not_associated": "Channel or Server are not associated with any Server/Channel.",
}

from flask import Flask, jsonify, request
from IAWRtypes._QueueManager import QueueManager
import requests, os
from dotenv import load_dotenv

#set the manager
from queue_manager import queue_manager  #importa a instância compartilhada

#import types
from IAWRtypes.SpawnPart import SpawnPartEntry
from IAWRtypes.OutputEditor import OutputEditorEntry
from IAWRtypes.ManagePlayer import ManagePlayerEntry
from IAWRtypes.SpawnAsset import SpawnAssetEntry

#test valuess
queue_manager.add_to_queue(
    OutputEditorEntry("12345").withType("addLine").withValue("Hello World!")
)
queue_manager.add_to_queue(
    SpawnPartEntry("12345")
        .withPosition("0, 0, 0")
        .withColor("Red")
        .withSize("1x1x1")
        .withName("Part Vermelhao")
)

############################################################################
EXPERIENCE_ID = "138227078356107"

channelToServerMap = {}

def validate_server(server_id: str, experience_id: str) -> bool:
    """
    Verifica se o servidor pertence à experiência Roblox especificada.
    """
    #verificar se já existia uma conexão com algum serverId ou canal antes para que não duplique
    if server_id in channelToServerMap:
        return False
    
    roblox_api_url = f"https://games.roblox.com/v1/games/{experience_id}/servers/Public"
    try:
        response = requests.get(roblox_api_url)
        #response.raise_for_status() ####################dps vejo isso
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar servidor com a API do Roblox: {e}")
        return False

    return True

def ServerOrChannelIsNotRegistered(fromChannel: str, serverId: str) -> bool:
    """
    Verifica se o canal ou servidor passado não existem.
    """
    return not (fromChannel in channelToServerMap.keys()) and not (serverId in channelToServerMap.items())

IAWRFlask = Flask(__name__)

@IAWRFlask.route("/connect")
def connect():
    fromChannel = request.args.get("fromChannel")
    serverId = request.args.get("serverId")
    if not fromChannel or not serverId:
        return jsonify({"error": "fromChannel and serverId are required"}), 400
    
    #verificar se um desses 2 valores já existem no dict channelToServerMap
    if not ServerOrChannelIsNotRegistered(fromChannel, serverId):
        return jsonify({"denied": f"you are trying to connect from a channel/server that is already connected"})
    
    if not validate_server(serverId, EXPERIENCE_ID):
        return jsonify({"error": "Invalid or unauthorized server ID"}), 403

    #salva os valores
    channelToServerMap[fromChannel] = serverId
    return jsonify({"success": True, "message": "Channel successfully linked to server"}), 200


@IAWRFlask.route("/get-server", methods=["GET"])
def get_server():
    fromChannel = request.args.get("fromChannel")
    if not fromChannel: return jsonify({"error": "fromChannel parameter is required"}), 400

    serverId = channelToServerMap.get(fromChannel)
    if not serverId: return jsonify({"error": "Channel not associated with any server"}), 404

    return jsonify({"serverId": serverId})


@IAWRFlask.route("/get-servers", methods=["GET"])
def get_servers():
    return jsonify({"servers": [{"serverId": server, "channel": channel} for channel, server in channelToServerMap.items()]})


@IAWRFlask.route("/")
def index():
    return """"IAWR Flask API.
    Para testar essa experiência, adicione o o bot através do link fornecido e linque o canal do chat de conexão com a experiencia que você estiver jogando.
    Use um servidor privado para que possa jogar o jogo.

    Link de convite do bot: https://discord.com/oauth2/authorize?client_id=1321246991807938600&permissions=8&integration_type=0&scope=bot
    """

@IAWRFlask.route("/queue") #/queue?fromChannel=12345&serverId=123456
def queue():
    fromConnectionChannel = request.args.get('fromChannel')
    if not fromConnectionChannel:
        return jsonify(queue_manager.get_queue())
    try:
        _ = int(fromConnectionChannel) #tenta converter para ver se é valido

        #se o argumento fromChannel for passado, também vai pedir o id do servidor da exériência (roblox)
        serverId = request.args.get('serverId')
        if not serverId:
            return jsonify({"denied": f"specifying a connection channel, you must identify wich server you will be using the queues from."})
        
        if ServerOrChannelIsNotRegistered(fromConnectionChannel, serverId):
            return jsonify({"error": "Channel/server are not associated with any channel/server"}), 404
        
        if not validate_server(serverId, EXPERIENCE_ID):
            return jsonify({"denied": f"Invalid or unauthorized server ID"}), 403
        
        return jsonify(queue_manager.take_queue(fromConnectionChannel))
    except Exception:
        return jsonify({"error": f"Invalid fromChannel value: '{fromConnectionChannel}'"})


def RunIAWRFlask():
    from waitress import serve
    serve(IAWRFlask, host='0.0.0.0', port=80)

    ##local
    #IAWRFlask.run(host="0.0.0.0", port=5000)
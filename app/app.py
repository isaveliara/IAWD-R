from flask import Flask, jsonify, request
from IAWRtypes._QueueManager import QueueManager

#set the manager
from queue_manager import queue_manager  #importa a instância compartilhada

#import types
from IAWRtypes.SpawnPart import SpawnPartEntry
from IAWRtypes.OutputEditor import OutputEditorEntry
from IAWRtypes.ManagePlayer import ManagePlayerEntry

#test values
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
queue_manager.add_to_queue(
    ManagePlayerEntry("09876")
        .killPlayer(123456789)
)

IAWRFlask = Flask(__name__)

@IAWRFlask.route("/")
def index():
    return """"IAWR Flask API.
    Para testar essa experiência, adicione o o bot através do link fornecido e linque o canal do chat de conexão com a experiencia que você estiver jogando.
    Use um servidor privado para que possa jogar o jogo.

    Link de convite do bot: https://discord.com/oauth2/authorize?client_id=1321246991807938600&permissions=8&integration_type=0&scope=bot
    """

@IAWRFlask.route("/queue") #/queue?fromChannel=12345
def queue():
    fromConnectionChannel = request.args.get('fromChannel')
    if not fromConnectionChannel:
        return jsonify(queue_manager.get_queue())
    try:
        _ = int(fromConnectionChannel)
        return jsonify(queue_manager.take_queue(fromConnectionChannel))
    except Exception:
        return jsonify({"error": f"Invalid fromChannel value: '{fromConnectionChannel}'"})


def RunIAWRFlask():
    #from waitress import serve
    #serve(IAWRFlask, host='0.0.0.0', port=80)

    ##local
    IAWRFlask.run(host="0.0.0.0", port=5000)
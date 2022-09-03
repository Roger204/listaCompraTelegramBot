import telepot
import time

compraFile = "lista.txt"
startText = "Bot para compartir una lista de la compra con \
 varias personas, ademas permite limitar la utilizacion del bot solo a quien se decida,\
 los comandos soportados son:\n\n\
    /ad: Add -> Añadir nuevo elemento a la lista\n\
    /pr: Print -> Retorna la lista actual\n\
    /dl: Delete -> Borra un elemento de la lista\n\
    /cl: Clear -> Borra toda la lista"

### La lista siguiente permite filtrar los participantes mediante su identificador chat_id \
### para saber el chat id del participante, este se imprime cuando el participante contacta con el bot\
### tan solo haria falta añadirlo aqui

ListaChatIds = ['TODO: Añadir los chat_ids para filtrar -> chat_id1, chat_id2, chat_id3']

def checkChatIds(chatid):
    return chatid in ListaChatIds

def parser(cmd):
    if(cmd[0] == "/"):
        cmd = cmd[1:]
    if(cmd.lower() == "ad"):
        return "ad"
    if(cmd.lower() == "pr"):
        return "pr"
    if(cmd.lower() == "dl"):
        return "dl"
    if(cmd.lower() == "cl"):
        return "cl"
    if(cmd.lower() == "start"):
        return "start"
    else:
        return "none"

def toAdd(element):
    print("Anadiendo " + element)
    oCompra = open(compraFile,"a")
    oCompra.write(element + "\n")
    oCompra.close()

def handle(msg):
    chat_id=msg['chat']['id']
    recCommand = msg['text']
    command = parser(recCommand.split()[0])
    print("chatid:     " + str(chat_id))
    if(command == 'ad' or command == 'dl'):
        if(len(recCommand.split()) <= 1):
            bot.sendMessage(chat_id, 'No se ha podido leer ningun elemento')
            return
        if(len(recCommand.split()) > 20):
            bot.sendMessage(chat_id, 'Elemento demasiado largo')
            return
        if(len(recCommand.split()) > 1):
            element = recCommand[3:]
        if(len(element)>20):
            bot.sendMessage(chat_id, 'Elemento demasiado largo')
            return
        if(element.isalpha() == False):
            bot.sendMessage(chat_id, 'No se ha borrado ningun elemento')
            print("texto invalido, solo se aceptan letras")
            return

    ## Command Parser ##
    print('Got command: %s ' % command)

    ## Start Command ##
    if(command == 'start'):
        bot.sendMessage(chat_id,startText)

    if(checkChatIds(chat_id) == False):
        return

    ## Add Command ##
    elif (command == 'ad'):
        toAdd(element)
        bot.sendMessage(chat_id,'Anadido: ' + element)

    ## Print Command ##
    elif(command == 'pr'):
        print("Print")
        LlistaToPrint = 'Hay que comprar: \n'
        oCompra = open(compraFile,"r")
        c = 0
        for line in oCompra:
            c = c+1
            LlistaToPrint = LlistaToPrint + ' ' + str(c) + '. ' + line
        bot.sendMessage(chat_id, LlistaToPrint)
        oCompra.close()

    ## Clear Command ##
    elif(command == 'cl'):
        open(compraFile, "w").close()
        bot.sendMessage(chat_id, 'La lista se ha borrado correctamente')

    ## Delete Command ##
    elif(command == 'dl'):
        newCompraArray = []
        try:
            oCompra = open(compraFile,"r")
            flagElement = 0
            elementoBorrado = ''
            for line in oCompra:
                if(line.find(element) == -1):
                    newCompraArray.append(line)
                else:
                    flagElement = 1
                    elementoBorrado = line
            oCompra.close()
            oCompra = open(compraFile,"w")
            for i in range(len(newCompraArray)):
                oCompra.write(newCompraArray[i])
            del newCompraArray[:]
            if(flagElement == 0):
                bot.sendMessage(chat_id, 'Elemento no encontrado')
            else:
                bot.sendMessage(chat_id,'Se ha borrado: ' + elementoBorrado)
        except ValueError:
            bot.sendMessage(chat_id, 'Elemento no encontrado')
            return
    else:
        bot.sendMessage(chat_id, 'Unknown command')

bot = telepot.Bot('TODO: Añadir aqui el token con formato parecido a xxxx:yyyyy-zzzzz')
bot.message_loop(handle)

while 1:
    #Should never reach here
    time.sleep(10)
import json
from datetime import datetime, timezone

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat_server import models


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.chat_id = (
            None  # inicijalno user nije otvorio ni jedan chat, a la whatsapp web
        )
        user = self.scope["user"]
        self.idkor = user.idkor
        print("CONNECTED")
        print(self.idkor)
        print(user)
        await self.channel_layer.group_add(
            # dodajemo korisnika u grupu idkor, da bi mogli da saljemo poruke iz servera
            "U" + str(self.idkor),
            self.channel_name,
        )
        await self.send(text_data=json.dumps({"status": "connection OK"}))

    async def disconnect(self, code):
        if self.chat_id:
            await self.channel_layer.group_discard(
                # izbacujemo korisnika iz grupe, ako je u nekoj grupi
                str(self.chat_id),
                self.channel_name,
            )

            await self.channel_layer.group_discard(
                # izbacujemo korisnika iz grupe idkor
                "U" + str(self.idkor),
                self.channel_name,
            )

    async def receive(self, text_data):  # text dolazi u server iz clienta
        event = json.loads(text_data)
        type = event["type"]
        if type == "open_chat":
            self.chat_id = event["chat_id"]
            print("RECEIVE OPEN, my chat id", self.chat_id, "my id", self.idkor)
            await self.channel_layer.group_add(  # dodajemo korisnika u grupu
                str(self.chat_id), self.channel_name
            )
        elif type == "close_chat":
            print("RECEIVE CLOSE, my chat id", self.chat_id, "my id", self.idkor)
            await self.channel_layer.group_discard(str(self.chat_id), self.channel_name)  # izbacujemo korisnika iz grupe
            self.chat_id = None
        elif type == "chat":
            message = event["message"]
            prep = await sync_to_async( models.Prepiska.objects.filter )(idpre=self.chat_id)
            prep = await sync_to_async( prep.first )()
            redbr = await sync_to_async( models.Poruka.objects.filter )(idpre=prep)
            redbr = await sync_to_async ( redbr.count )() + 1
            idsender = await sync_to_async(models.Korisnik.objects.filter)(idkor=self.idkor)
            idsender = await sync_to_async(idsender.first)()
            poruka = models.Poruka(
                idsender=idsender,
                idpre=prep,
                tekst=message,
                status="U",
                redbr=redbr,
                time=datetime.now(timezone.utc),
            )
            await sync_to_async ( poruka.save )()
            print("RECEIVE MESSAGE, my chat id", self.chat_id, "my id", self.idkor)
            await self.channel_layer.group_send(
                # saljemo poruku iz servera u grupu
                str(self.chat_id),
                {
                    "type": "chat.message",
                    "message": message,
                    "redbr": redbr,
                    "sender": self.idkor,
                    "time": poruka.time,
                },
            )
            other_user_id = (
                prep.idkor1_id if self.idkor == prep.idkor2_id else prep.idkor2_id
            )
            print("OTHER USER ID", other_user_id)
            print("MY ID", self.idkor)
            print("SENDING UPDATE TO OTHER USER")
            await self.channel_layer.group_send(
                # saljemo poruku iz servera u grupu
                "U" + str(other_user_id),
                {
                    "type": "update",
                    "sender": self.idkor,
                },
            )
    async def chat_message(self, event):  # event tipa chat.message dolazi u server iz grupe
        type = event["type"]
        print("CHAT MESSAGE")
        sender = event["sender"]
        if sender == self.idkor:
            print("SEND MESSAGE MY ID IS SENDER, my id", self.idkor)
            print(event)
            return
        if (
            type == "chat.message"
        ):  # ako je tip chat, poslata je u grupu chata sobe, prosledjuje klijentu se kao poruka
            message = event["message"]
            redbr = event["redbr"]

            print("SEND MESSAGE, my chat id", self.chat_id, "my id", self.idkor)
            poruka = await sync_to_async ( models.Poruka.objects.filter )(
                idpre=self.chat_id, redbr=redbr
            )
            poruka = await sync_to_async ( poruka.first )()
            poruka.status = "R"
            await sync_to_async ( poruka.save )()
            import json

            time = event["time"]
            time = json.dumps(time.isoformat())
            time = time.split(".")[0]
            time.replace("T", "@")
            print(time)
            await self.send(
                text_data=json.dumps({"type": "chat", "message": message, "time": time})
            )

    async def update(self, event):  # event tipa update dolazi u server iz grupe
        from budivolonter import utils

        unread_msgs = await sync_to_async ( utils.unread_msg )(self.idkor)
        print("UPDATE")
        await self.send(text_data=json.dumps({"type": "update", "unread_msgs": unread_msgs}))

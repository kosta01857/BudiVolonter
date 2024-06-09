from django.http import HttpRequest

from budivolonter import models
from budivolonter.models import Aktivnost, Korisnik


#Djordje Sarovic
def getCurrentUser(request:HttpRequest) -> Korisnik|None:
    if request.user.is_anonymous:
        return None
    return models.Korisnik.objects.filter(email=request.user.get_username()).first()

#Kosta Novokmet
def checkLogin(request:HttpRequest) -> bool:
    if request.user.is_authenticated: return True
    else: return False

#Kosta Novokmet
#vraca na kom kontinentu je neka drzava 
def getContinent(country) -> dict:
    from .locations import continents, countries
    for contient,countries in continents.items():
        if country in countries: return contient
    return None


#Kosta Novokmet
#vraca listu svih drzava na svetu
#za potrebe biranja drzava kada se pravi aktivnost
def getCountries() -> tuple:
    from .locations import countries
    return countries


#Kosta Novokmet
#proverava da li je datum prosao 
#ako je datum prosao, vraca true 
from datetime import date


def datePassed(date:date) -> bool:
    curr_date = date.today()
    if (curr_date > date): 
       return True
    return False



#Kosta Novokmet
#pravi listu aktivnosti, svaka aktivnost je recnik
def loadActivities(acts:list[Aktivnost],request) -> list[dict]:
    from . import model_funcs
    idkor = getCurrentUser(request).idkor
    act_list= []
    for act in acts:
        app = model_funcs.getApplicationsForActVol(idkor=idkor,idakt=act.idakt)
        print(idkor,act.idakt,app)
        act_data               = {}
        oblasti                = list(act.oblasti.all().values_list(flat=True))
        zahtevi                = model_funcs.getActivityReqs(act.idakt)
        act_data['status_prijave'] =  app.get('status') if app != None else 'X'
        act_data['id']         = act.idakt
        act_data['naziv']      = act.naziv
        act_data['opis']       = act.opis
        act_data['oblasti']    = oblasti
        act_data['zahtevi']    = zahtevi
        act_data['brmesta']    = act.brmesta
        act_data['datumStart'] = act.datumod
        act_data['datumEnd']   = act.datumdo
        act_data['datumRok']   = act.datumrok
        act_data['drzava']     = act.lokacija.drzava
        act_data['kontinent']  = act.lokacija.kontinent
        act_data['org']        = act.idorg.ime
        act_list.append(act_data)
    return act_list

#Kosta Novokmet
def loadMessages(messages:list[models.Poruka]) -> list[dict]:
    from . import model_funcs
    message_list = []
    for message in messages:
        time                   = message.time.isoformat().split('+')[0]
        time                   = time.replace('T','@')
        message_data           = {}
        message_data['sender'] = message.idsender_id
        message_data['text']   = message.tekst
        message_data['time']   = time
        message_data['status'] = message.status
        message_data['order']  = message.redbr
        message_list.append(message_data)
    return message_list

    


#Kosta Novokmet
def loadChats(chats:list[models.Prepiska],id:int) -> list[dict]:
    from . import model_funcs
    chat_list = []
    for chat in chats:
        chat_data = {}
        messages_unread = models.Poruka.objects.filter(idpre=chat.idpre, status='U', idsender_id=chat.idkor1_id if id == chat.idkor2_id else chat.idkor2_id).count()
        chat_data['messages_unread'] = messages_unread
        chat_data['user'] = f'{chat.idkor2.ime} {chat.idkor2.prezime if chat.idkor2.prezime else ""}' if id == chat.idkor1_id else f'{chat.idkor1.ime} {chat.idkor1.prezime if chat.idkor1.prezime else ""}' #(yes i know its bad)
        chat_data['id'] = chat.idpre
        chat_list.append(chat_data)

    return chat_list

#Kosta Novokmet
def getNavbar(request) -> str:
    usr = getCurrentUser(request)
    if usr is None:
        user_type= 'UNR'
    else:
        user_type = usr.tip
    if(user_type == 'O'):
        with open('./budivolonter/html/navbar_org.html','r') as file:
            return file.read()
    elif (user_type == 'V'):
        with open('./budivolonter/html/navbar_vol.html','r') as file:
            return file.read()
    elif (user_type == 'A'):
        with open('./budivolonter/html/navbar_admin.html','r') as file:
            return file.read()
    elif(user_type == 'UNR'):
        with open('./budivolonter/html/navbar_unreg.html','r') as file:
            return file.read()

#Kosta Novokmet
def getFooter() -> str:
    with open('./budivolonter/html/footer.html','r') as file:
        return file.read()
    
#Natalija Vujnic
#vraca broj godina na osnovu datuma rodjenja
def getAge(dateOfBirth) -> int:
    from datetime import datetime
    if isinstance(dateOfBirth, str):
        dateOfBirth = datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
    today = date.today()
    age   = today.year-dateOfBirth.year
    if(today.month,today.day)<(dateOfBirth.month,dateOfBirth.day):
        age -= 1
    return age

def unread_msg(id) -> int:
    from . import model_funcs
    chats = model_funcs.getChats(id);
    from .utils import loadChats
    chat_dict = loadChats(chats,id)
    sum = 0
    for chat in chat_dict:
       sum += chat['messages_unread']
    return sum

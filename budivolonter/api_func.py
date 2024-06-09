from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect

from budivolonter import models
from budivolonter.utils import getCurrentUser

from . import model_funcs


#kosta novokmet
#vraca sve aktivnosti organizacije 
#org = ona ciji se profil gleda
def fetch_activities_org(request:HttpRequest) -> JsonResponse:
    from . import utils
    idkor                    = model_funcs.getUserId(request.GET.get('id'))
    active_activities        = model_funcs.getActiveActivitiesOrg(idkor)
    archived_activities      = model_funcs.getArchivedActivitiesOrg(idkor)
    active_activities_list   = utils.loadActivities(active_activities,request)
    archived_activities_list = utils.loadActivities(archived_activities,request)
    for act in archived_activities_list:
        reviews = model_funcs.getApplicationsForAct(idakt=act.get('id'),finished=True,status='A')
        act['reviews'] = reviews
    
    return JsonResponse({'active_activities':active_activities_list,'archived_activities':archived_activities_list})


#kosta novokmet
#vraca sve aktivnosti na kojima je volonter 
#volonter = onaj ciji se profil gleda
def fetch_activities_vol(request) -> JsonResponse:
    from . import utils
    idkor      = model_funcs.getUserId(request.GET.get('id'))
    print(idkor)
    activities = model_funcs.getActivitiesVol(idkor)
    activities_list = utils.loadActivities(activities,request)
    for act in activities_list:
        review = model_funcs.getApplicationsForActVol(idakt=act.get('id'),idkor=idkor,finished=True)
        if review is None: act['review'] = 'null'
        else : act['review'] = review
    return JsonResponse({'activities':activities_list})


#kosta novokmet
#updatuje slobodna mesta aktivnosti
def update_free_spaces(request:HttpRequest) -> JsonResponse:
    import json
    json_data = json.loads(request.body.decode('utf-8'))
    val       = json_data['val']
    aktId     = json_data['idakt']
    model_funcs.updateFreeSpaces(val,aktId)
    return JsonResponse({'message': 'Data received successfully'}, status=200)

#Djordje Sarovic
#prihvata ili odbija prijavu
def resolveApplication(request:HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    id      = request.POST.get('id', None)
    status  = request.POST.get('status', None)
    prijava = model_funcs.getApplicationById(id)
    prijava.status = status
    prijava.save()
    return HttpResponse('OK')


#Djordje Sarovic
#servira rezime prijave
def download(request:HttpRequest) -> HttpResponse:
    if getCurrentUser(request) is None:
        return redirect('login')
    elif getCurrentUser(request).tip == 'V':
        return redirect('welcome') #todo redirect to error 403 forbidden page
    idPri = request.GET.get('id', None)
    if idPri is None:
        return redirect('welcome') #todo redirect to error 404 page
    prijava = model_funcs.getApplicationById(idPri)
    if prijava is None:
        return redirect('welcome') #todo redirect to error 404 page
    if prijava.idakt.idorg_id != getCurrentUser(request).idkor:
        return redirect('welcome') #todo redirect to error 403 forbidden page
    response = HttpResponse(prijava.rezime, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rezime_'+prijava.idvol.ime+'_'+prijava.idvol.prezime+'_za_'+prijava.idakt.naziv+'.pdf"'
    return response



#Kosta Novokmet
def get_chats(request:HttpRequest) -> JsonResponse:
    from .utils import checkLogin, getCurrentUser, loadChats
    id    = getCurrentUser(request).idkor
    chats = loadChats(model_funcs.getChats(id),id)
    return JsonResponse({'chats':chats})
    

def get_messages(request:HttpRequest) -> JsonResponse:
    from .utils import loadMessages
    id        = int(request.GET.get('id'))
    id_reader = getCurrentUser(request).idkor
    messages  = loadMessages(model_funcs.getMessages(id, id_reader))
    return JsonResponse({'messages':messages})


#Kosta Novokmet
def open_chat(request:HttpRequest) -> HttpResponse:
    from .utils import getCurrentUser
    id          = request.POST.get('id')
    current_usr = getCurrentUser(request)
    curr_id     = current_usr.idkor
    from .model_funcs import insertChat
    print(curr_id,id)
    insertChat(curr_id,id)
    return HttpResponse('OK')
    


#Kosta Novokmet
def get_unread(request:HttpRequest) -> JsonResponse:
    from .utils import getCurrentUser, unread_msg
    id = getCurrentUser(request).idkor
    return JsonResponse({'count':unread_msg(id)})


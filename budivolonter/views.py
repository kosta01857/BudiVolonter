from datetime import datetime
from django.contrib.auth import login, logout
from django.http import HttpRequest 
from django.shortcuts import HttpResponse, redirect, render
from . import model_funcs
from .utils import getCurrentUser


#Kosta Novokmet
#renderuje welcome page
def welcome(request:HttpRequest) -> HttpResponse:
    from . import utils
    context = {}
    context['navbar'] = utils.getNavbar(request)
    context['footer'] = utils.getFooter()
    return render(request,'main_page.html',context) 

def register_choice(request):
    from . import utils
    if utils.getCurrentUser(request) is not None:
        return HttpResponse('Access Forbidden', status=403)
    context = {}
    context['navbar'] = utils.getNavbar(request)
    context['footer'] = utils.getFooter()
    return render(request,'reg_choose.html',context) 



#Kosta Novokmet
#ubacuje novu aktivnost u bazu
def open_activity(request:HttpRequest)-> HttpResponse:
    from . import utils
    if utils.checkLogin(request):
        if utils.getCurrentUser(request) is None:
            return redirect('login')
        elif utils.getCurrentUser(request).tip == 'V':
            return redirect('welcome') #todo redirect to error 404 page
        if(request.method == 'POST'):
            parameters   = request.POST
            cats         = parameters.getlist('categories')
            reqs         = parameters.get('reqs').strip().replace('\r','').split('\n')
            name         = parameters['name']
            desc         = parameters['desc']
            spots        = int(parameters['spots'])
            startDate    = parameters['startDate']
            endDate      = parameters['endDate']
            deadlineDate = parameters['deadlineDate']
            country      = parameters['country']
            city         = parameters['city']
            user         = getCurrentUser(request)
            model_funcs.insertActivity(user,name,desc,spots,startDate,endDate,deadlineDate,cats,country,city,reqs)
            from . import utils
            context = {
                    'countries': utils.getCountries,
                    'status':    'USPESNO DODATA AKTIVNOST!',
                    'cats':      model_funcs.getCategoryNames(),
                    'navbar':    utils.getNavbar(request),
                    'footer':    utils.getFooter()
                    }
            return render(request,'open_activity.html',context)
        else:
            from . import utils
            context = {
                    'countries': utils.getCountries,
                    'status':    '',
                    'cats':      model_funcs.getCategoryNames(),
                    'navbar':    utils.getNavbar(request),
                    'footer':    utils.getFooter()
                    }
            return render(request,'open_activity.html',context)
    else:return redirect('login')

#Natalija Vujnic
#funcija za prikaz sopstvenog profila
def display_my_profile(request):
    from .utils import checkLogin
    if checkLogin(request):
        id = getCurrentUser(request).idkor
        return redirect(f'/budivolonter/profile?id={id}')
    else:
        return redirect('login')

#Natalija Vujnic
#prikaz profila korisnika na osnovu id prosledjenog u query stringu
def display_profile(request:HttpRequest)-> HttpResponse:
    from .utils import checkLogin
    if checkLogin(request):
        from . import utils
        id           = request.GET['id']
        korisnik     = model_funcs.getUsrById(id)
        tipKorisnika = korisnik.tip
        tipProfila   = getCurrentUser(request).tip
        if tipKorisnika == 'O':
            posalji = False
            if tipProfila == 'V': posalji = True
            context = {
                    'korisnik':       korisnik,
                    'navbar':         utils.getNavbar(request),
                    'id':             request.GET['id'],
                    'curr_id':        getCurrentUser(request).idkor,
                    'posalji_poruku': posalji,
                    'footer':    utils.getFooter()
                    }
            return render(request, 'org_profile.html', context)
        elif tipKorisnika=='V':
            interesi=model_funcs.getInterests(korisnik.idkor)
            posalji=False
            if tipProfila=='O': posalji=True
            context = {
                    'korisnik':       korisnik,
                    'navbar':         utils.getNavbar(request),
                    'interesi':       interesi,
                    'id':             request.GET['id'],
                    'curr_id':        getCurrentUser(request).idkor,
                    'age':            utils.getAge(korisnik.datumrodj),
                    'posalji_poruku': posalji,
                    'footer':    utils.getFooter()
                    }
            return render(request, 'volonteer_profile.html', context)
        elif tipKorisnika == 'A':
            stranica='admin_start.html'
            return render(request, stranica,{'navbar':utils.getNavbar(request)})
    return redirect('login')

#Anja Mihajlov
#Koristi se za insert nove organizacije u bazu
def reg_org(request: HttpRequest)-> HttpResponse:
    from . import utils
    if utils.getCurrentUser(request) is not None:
        return redirect('welcome')
    from . import utils
    context = {
            'navbar': utils.getNavbar(request),
            'footer':    utils.getFooter()
            }
    if(request.method == 'POST'):
        parametri = request.POST
        ime       = parametri['nazivOrganizacije']
        pib       = parametri['pib']
        telefon   = parametri['telefon']
        email     = parametri['email']
        lozinka   = parametri['lozinka']

        if  model_funcs.UsrFromTel(tel=telefon,exists=True) or model_funcs.UsrFromPib(pib = pib,exists=True) or  model_funcs.UsrFromEmail(email=email,exists=True):
                poruka = "Već postoji korisnik sa datim telefonom, PIB-om ili e-mailom."

        else:
            poruka = "Organizacija je uspešno registrovana."
            model_funcs.insertOrganization(ime,pib,telefon,email,lozinka)
        context['poruka'] = poruka

        return render(request,'reg_org.html', context)

    return render(request, 'reg_org.html',context)


#Anja Mihajlov
#Registracija volontera
def reg_vol(request: HttpRequest)-> HttpResponse:
    from . import utils
    if utils.getCurrentUser(request) is not None:
        return redirect('welcome')
    context = {
                'cats':   model_funcs.getCategoryNames(),
                'navbar': utils.getNavbar(request),
                'footer':    utils.getFooter()
                }
    if(request.method == 'POST'):
        parametri      = request.POST
        ime            = parametri['ime']
        prezime        = parametri['prezime']
        datumRodj      = parametri['datumRodjenja']
        email          = parametri['email']
        lozinka        = parametri['lozinka']
        cats           = parametri.getlist('categories')

        #provera za godine
        datum_rodjenja = datetime.strptime(datumRodj, "%Y-%m-%d")
        danas          = datetime.now()
        godine         = danas.year - datum_rodjenja.year - ((danas.month, danas.day) < (datum_rodjenja.month, datum_rodjenja.day))


        if model_funcs.UsrFromEmail(email=email,exists=True):
            context = {
                'poruka': "Već postoji korisnik sa datim e-mailom.",
                'cats':   model_funcs.getCategoryNames()
                }
        elif godine<16 or godine>100:
            context = {
                'poruka': "Ne spadate u starosnu grupu za volontiranje",
                'cats':   model_funcs.getCategoryNames(),
                'navbar': utils.getNavbar(request),
                'footer':    utils.getFooter()
                }

        else:
            model_funcs.insertVolunteer(ime,prezime,datumRodj,email,lozinka,cats)
            context = {
                'poruka': "Volonter je uspešno registrovan.",
                'cats':   model_funcs.getCategoryNames(),
                'navbar': utils.getNavbar(request),
                'footer':    utils.getFooter()
                }

        from . import utils
        return render(request,'reg_vol.html', context)

    return render(request, 'reg_vol.html', context)

#Djordje Sarovic
#funkcija za prikaz stranice za login
def login_page(request:HttpRequest)-> HttpResponse:
    from . import utils
    if utils.getCurrentUser(request) is not None:
        return redirect('welcome')
    if request.method == 'GET':
        return render(request, 'login.html',{'navbar': utils.getNavbar(request),

                                            'footer':    utils.getFooter()
                                             })
    else:
        email    = request.POST['email']
        password = request.POST['password']
        user     = model_funcs.UsrFromEmail(email=email)
        if user:
            if user.check_password(password):
                login(request, user)
                if user.tip =='A': #dodala sam ti ova dva reda zbog admina
                    return redirect('admin_start')
                return redirect('my_profile')
            else:
                return render(request, 'login.html', {'errorPassword':'Pogresna sifra','navbar': utils.getNavbar(request),
                                                      'footer':    utils.getFooter()
                                                      })
        else:
            return render(request, 'login.html', {'errorEmail':'Pogresan email','navbar': utils.getNavbar(request),
                                                  'footer':    utils.getFooter()
                                                  })
#Djordje Sarovic
def do_logout(request)-> HttpResponse:
    logout(request)
    return redirect('login')

#Djordje Sarovic
def activity_form(request:HttpRequest)-> HttpResponse:
    if getCurrentUser(request) is None:
        return redirect('login')
    elif getCurrentUser(request).tip == 'O':
        return redirect('welcome') #todo redirect to error 404 page
    from . import utils
    idAkt = request.GET.get('id', None)
    if idAkt is None:
        return redirect('welcome') #todo redirect to error 404 page
    aktivnost = model_funcs.getActivityById(idAkt)
    organizacija =model_funcs.getUsrById(aktivnost.idorg_id)
    context = {
        'naziv':            aktivnost.naziv,
        'datumOd':          aktivnost.datumod,
        'datumDo':          aktivnost.datumdo,
        'organizacija_ime': organizacija.ime,
        'navbar':           utils.getNavbar(request),
        'footer':           utils.getFooter()
    }
    if request.method == 'GET':
        return render(request, 'activity_form.html', context)
    else:
        user = getCurrentUser(request)
        aktivnost = model_funcs.getActivityById(idAkt)
        if model_funcs.getApplicationsForActVol(idkor=user, idakt=aktivnost.idakt,exists=True):
            context['error'] = 'Vec ste se prijavili na ovu aktivnost'
            return render(request, 'activity_form.html', context)
        pismo = request.POST['pismo']
        if pismo == '':
            context['error'] = 'Morate uneti pismo'
            return render(request, 'activity_form.html', context)
        rezimeFile = request.FILES.get('rezime', None)
        model_funcs.insertApplication(idvol=user, idakt=idAkt, pismo=pismo, rezimeFile=rezimeFile)
        context['success'] = 'Uspesno ste se prijavili na aktivnost'
        return render(request, 'activity_form.html', context)

#Djordje Sarovic
def view_applications(request:HttpRequest):
    if getCurrentUser(request) is None:
        return redirect('login')
    elif getCurrentUser(request).tip == 'V':
        return redirect('welcome') #todo redirect to error 403 forbidden page
    from . import utils
    idAkt = request.GET.get('id', None)
    if idAkt is None:
        return redirect('welcome') #todo redirect to error 404 page
    aktivnost = model_funcs.getActivityById(idAkt)
    if aktivnost is None:
        return redirect('welcome') #todo redirect to error 404 page
    if aktivnost.idorg_id != getCurrentUser(request).idkor:
        return redirect('welcome') #todo redirect to error 403 forbidden page
    prijave = model_funcs.getApplicationsForAct(idakt=idAkt,status="O")
    context = {
        'naziv':   aktivnost.naziv,
        'prijave': prijave,
        'navbar':  utils.getNavbar(request),
        'footer':  utils.getFooter()
    }
    print(context)
    return render(request, 'applications_view.html', context)



"""Kosta Novokmet, Djordje Sarovic"""
def inbox(request:HttpRequest):
    print("returining html")
    from .utils import checkLogin, getCurrentUser, getNavbar,getFooter
    if checkLogin(request):
        id = getCurrentUser(request).idkor
        return render(request,'prepiske.html', {'navbar':getNavbar(request), 'user_id':id,
                                                'footer':    getFooter()
                                                })
    else: return redirect('login')
    

#Natalija Vujnic
#funkcija za azuriranje korisnickog profila
def edit_profile(request:HttpRequest)-> HttpResponse:
    ulogovan = request.user.is_authenticated
    if ulogovan:
        from . import utils
        korisnik=utils.getCurrentUser(request)
        tipKorisnika=korisnik.tip
        context = {
                    'korisnik': korisnik,
                    'navbar':   utils.getNavbar(request),
                    'footer':    utils.getFooter()
                    }
        if request.method == 'POST':
            if tipKorisnika=='O':
                newIme = request.POST.get('ime')
                newPib = request.POST.get('pib')
                newTel = request.POST.get('telefon')
                if model_funcs.UsrFromTel(tel=newTel,exists=True) and newTel!=korisnik.telefon:
                    poruka = "Već postoji korisnik sa datim telefonom."
                    context['poruka'] = poruka
                elif model_funcs.UsrFromPib(pib=newPib,exists=True) and int(newPib)!=korisnik.pib:
                    poruka = "Već postoji korisnik sa datim PIB-om."
                    context['poruka'] = poruka
                else:
                    model_funcs.editOrganization(korisnik,newIme,newPib,newTel)
                    return redirect('my_profile')
            elif tipKorisnika=='V':
                newIme     = request.POST.get('ime')
                newPrezime = request.POST.get('prezime')
                newDatum   = request.POST.get('datumRodjenja')
                newCats    = request.POST.getlist('interes')
                godine=utils.getAge(newDatum)
                if godine<16 or godine>100:
                    poruka = "Ne spadate u starosnu grupu za volontiranje."
                    context['poruka'] = poruka
                else:
                    model_funcs.editVolunteer(korisnik,newIme,newPrezime,newDatum,newCats)
                    return redirect('my_profile')
        if tipKorisnika == 'O':
            return render(request, 'org_edit.html', context)
        elif tipKorisnika == 'V':
            sviInteresi      = model_funcs.getAllInteresIds()
            interesiKorisnik = model_funcs.getInterestsIds(korisnik.idkor)
            interesi         = []
            for interes in sviInteresi:
                interesFormat = {
                    'id':      interes.idobl,
                    'name':    interes.oblast,
                    'checked': interes.idobl in interesiKorisnik
                    }
                interesi.append(interesFormat)
            context['interesi']=interesi
            return render(request, 'vol_edit.html', context)
    else:
        return redirect('login')

#Anja Mihajlov
#Koristi se za pretragru organizacija
def search_org(request: HttpRequest)-> HttpResponse:
    name_search = request.GET.get('name_search')
    if name_search:
        orgs = model_funcs.filterOrganizationsName(name_search)
    else:
        orgs = model_funcs.getAllOrganizations()

    from . import utils
    context = {
            'orgs':   orgs,
            'navbar': utils.getNavbar(request),
            'footer':    utils.getFooter()
            }
    return render(request, 'search_org.html', context)


#Anja Mihajlov
#Koristi se za pretragu volontera
def search_vol(request: HttpRequest)-> HttpResponse:
    ulogovan = request.user.is_authenticated
    if ulogovan:

        name_search = request.GET.get('name_search')

        vols = model_funcs.getAllVolunteers()
        if name_search:
            vols = model_funcs.filterVolunteersName(name_search,vols)

        experience = request.GET.get('volunteer_experience')
        
        if experience == 'ne':
            vols = model_funcs.filterVolunteerExperience(False, vols)
        elif experience == 'da':
            vols = model_funcs.filterVolunteerExperience(True, vols)

        cats = request.GET.getlist('interes')
        if (cats):
            vols = model_funcs.filterVolunteerCategories(vols,cats)

        interesi = model_funcs.getAllInteresIds()
        from . import utils
        context = {
            'vols':     vols,
            'navbar':   utils.getNavbar(request),
            'interesi': interesi,
            'footer':    utils.getFooter()
            }
        return render(request, 'search_vol.html', context)
    else:
        return redirect('login')

#Anja Mihajlov
#Izbor pretrage korisnika
def search_choose(request: HttpRequest)-> HttpResponse:
    from . import utils
    context = {
            'navbar': utils.getNavbar(request),
            'footer':    utils.getFooter()
            }
    return render(request, 'choose_search.html', context)

#Natalija Vujnic
#ostavljanje recenzija volonterima sa profila organizacije
def review_volunteers(request: HttpRequest)-> HttpResponse:
    from . import utils
    if utils.checkLogin(request):
        id           = getCurrentUser(request).idkor
        korisnik     = model_funcs.getUsrById(id)
        tipKorisnika = korisnik.tip
        if tipKorisnika == 'O':
            if request.method == 'POST':
                parameters = request.POST
                ocena      = parameters['recommendation']
                komentar   = parameters['comment']
                idAkt      = parameters['idAkt']
                prijava    = parameters['prijava']
                model_funcs.writeCommentOrg(prijava,ocena,komentar)
            elif request.method == 'GET':
                idAkt = request.GET['id']
            prijave=model_funcs.getUnreviewedApplications(idAkt)
            vols=[]
            for prijava in prijave:
                volonter = model_funcs.getUserEmail(prijava.idvol)
                vol      = {
                    'idkor':     volonter.idkor,
                    'ime':       volonter.ime,
                    'prezime':   volonter.prezime,
                    'idPrijave': prijava.idpri
                    }
                vols.append(vol)
            context = {
                    'korisnik': korisnik,
                    'navbar':   utils.getNavbar(request),
                    'akt':      model_funcs.getActivityById(idAkt),
                    'vols':     vols,
                    'footer':    utils.getFooter()
                    }
            return render(request, 'org_review_volonteers.html', context)
    return redirect('login')

#Natalija Vujnic
#ostavljanje recenzija organizacijama sa profila volontera
def review_organizations(request: HttpRequest)-> HttpResponse: 
    from . import utils
    if utils.checkLogin(request):
        id           = getCurrentUser(request).idkor
        korisnik     = model_funcs.getUsrById(id)
        tipKorisnika = korisnik.tip
        if tipKorisnika == 'V':
            if request.method == 'POST':
                parameters = request.POST
                ocena      = parameters['recommendation']
                komentar   = parameters['comment']
                prijava    = parameters['prijava']
                model_funcs.writeCommentVol(prijava,ocena,komentar)
            prijave = model_funcs.getUnreviewedOrgs(id)
            orgs    = []
            for prijava in prijave:
                akt          = model_funcs.getActivityById(prijava.idakt_id)
                organizacija = model_funcs.getUserEmail(akt.idorg)
                org          = {
                    'idkor':     organizacija.idkor,
                    'ime':       organizacija.ime,
                    'idPrijave': prijava.idpri,
                    'aktName':   akt.naziv
                    }
                orgs.append(org)
            context = {
                    'korisnik': korisnik,
                    'navbar':   utils.getNavbar(request),
                    'orgs':     orgs,
                    'footer':    utils.getFooter()
                    }
            return render(request, 'vol_review_org.html', context)
    return redirect('login')

#Kosta Novokmet

def my_acts(request:HttpRequest):
    from .model_funcs import getAcceptedActs
    usr = getCurrentUser(request)
    acts = getAcceptedActs(usr)
    act_list= []
    for act in acts:
        act_data = {}
        oblasti =  model_funcs.getCategorisForActivity(act.idakt)
        zahtevi = model_funcs.getSkillsForActivity(act.idakt)
        act_data['idakt']        = act.idakt
        act_data['naziv']        = act.naziv
        act_data['opis']         = act.opis
        act_data['cats']         = oblasti
        act_data['skills']       = zahtevi
        act_data['brmesta']      = act.brmesta
        act_data['datumod']      = act.datumod
        act_data['datumdo']      = act.datumdo
        act_data['datumrok']     = act.datumrok
        act_data['drzava']       = act.lokacija.drzava
        act_data['mesto']        = act.mesto
        act_data['organizacija'] = act.idorg.ime
        act_data['idorg']        = act.idorg_id
        act_list.append(act_data)
    from . import utils
    context = {
            'navbar':   utils.getNavbar(request),
            'acts':     act_list,
            'footer':   utils.getFooter()
            }
    return render(request,'my_acts.html',context)


#Anja Mihajlov
#Pretraga aktivnosti
def search_activity(request: HttpRequest)-> HttpResponse:

    acts = model_funcs.getActiveActivities()
    '''
    vestine = request.GET.getlist('skill')
    acts = model_funcs.filterActBySkills(acts, vestine)
    '''
    datumod = request.GET.get('date_from')
    if datumod:
        acts = model_funcs.getActivitiesAfter(acts,datumod)

    datumdo = request.GET.get('date_to')
    if datumdo:
        acts = model_funcs.getActivitiesBefore(acts,datumdo)

    kontinent = request.GET.get('country')
    if kontinent:
        acts= model_funcs.getActivitiesContinent(acts,kontinent)
    area = request.GET.get('area')
    if area:
        acts = model_funcs.filterActsByCat(acts,area)
    korisnik = getCurrentUser(request)
    if korisnik is None:
        korisnik = 0

    act_list= []
    for act in acts:
        act_data = {}
        oblasti =  model_funcs.getCategorisForActivity(act.idakt)
        zahtevi = model_funcs.getSkillsForActivity(act.idakt)
        act_data['idakt'] = act.idakt
        act_data['naziv'] = act.naziv
        act_data['opis'] = act.opis
        act_data['cats'] = oblasti
        act_data['skills'] = zahtevi
        act_data['brmesta'] = act.brmesta
        act_data['datumod'] = act.datumod
        act_data['datumdo'] = act.datumdo
        act_data['datumrok'] = act.datumrok
        act_data['drzava'] = act.lokacija.drzava
        act_data['mesto'] = act.mesto
        act_data['organizacija'] = act.idorg.ime
        act_list.append(act_data)
    from . import utils
    context = {
            'korisnik': korisnik,
            'navbar':utils.getNavbar(request),
            'acts': act_list,
            #'skills': model_funcs.getAllSkills(),
            'cats': model_funcs.getAllCats(),
            'conts':['Afrika','Azija', 'Evropa','Severna Amerika', 'Okeanija','Južna Amerika'],
            'footer':    utils.getFooter()
            }
    return render(request, 'search_act.html', context)

#Anja Mihajlov
#Admin start, stranica gde brise korisnike i aktivnosti
#email je admin@bv.rs, sifra je Admin123
def admin_start(request: HttpRequest) -> HttpResponse:
    from . import utils
    if utils.checkLogin(request):
        tip = getCurrentUser(request).tip
        if(tip !='A'):
            return redirect('login')
        aktivnost =  request.GET.get('aktivnost')
        poruka =""
        email =  request.GET.get('email')
        if aktivnost:
            poruka = model_funcs.deleteAktivnost(aktivnost)
        if email:
            poruka = model_funcs.deleteUser(email)
        
        from . import utils
        context = {
                'navbar':utils.getNavbar(request),
                'poruka': poruka, 
                'footer':    utils.getFooter()
                }
        return render(request, 'admin_start.html', context)
    return redirect('login')

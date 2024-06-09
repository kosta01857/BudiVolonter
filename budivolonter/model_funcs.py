from django.db import transaction

from chat_server.models import Korisnik

from . import models


# Kosta Novokmet
# vraca sve korisnike kao listu objekata
def getUsers() -> list[models.Korisnik]:
    return list(models.Korisnik.objects.all())


def getUserId(id):
    return models.Korisnik.objects.filter(idkor=id).first().idkor


# Kosta Novokmet
# u bazu ubacuje novu aktivnost kao i sve propratne veze
def insertActivity(
    org, name, desc, spots, startD, endD, deadline, categories, country, city, reqs
) -> models.Aktivnost:
    with transaction.atomic():
        location = getLocation(country)
        activity = models.Aktivnost(
            idorg    = org,
            naziv    = name,
            opis     = desc,
            brmesta  = spots,
            datumod  = startD,
            datumdo  = endD,
            datumrok = deadline,
            mesto    = city,
            lokacija = location,
        )
        activity.save()
        for req_desc in reqs:
            req = models.Vestina(idakt=activity, opis=req_desc)
            req.save()
        for cat in categories:
            cat_obj = getCategoryObject(cat)
            print(cat_obj.oblast, cat_obj.idobl)
            belongs = models.Pripada(idakt=activity, idobl=cat_obj)
            belongs.save()
    return activity

# Kosta Novokmet
# vraca objekat Lokacija na osnovu drzave
def getLocation(country) -> models.Lokacija:
    result = models.Lokacija.objects.filter(drzava=country).first()
    if not result:
        from . import utils

        continent = utils.getContinent(country)
        location = models.Lokacija(drzava=country, kontinent=continent)
        location.save()
        return location
    return result


# Kosta Novokmet
# vraca listu imena svih kategorija
# potrebno za html ispis
def getCategoryNames() -> list:
    return list(models.Oblast.objects.all().values_list("oblast", flat=True))


# kosta Novokmet
# vraca objekat Oblasti na osnovu naziva Oblasti
# potrebno prilikom ubacivanja u bazu
def getCategoryObject(name) -> models.Oblast:
    return models.Oblast.objects.filter(oblast=name).first()


# Natalija Vujnic
# vraca interesovanja konkretnog korisnika
def getInterests(id) -> list:
    return models.ZanimaGa.objects.filter(idkor_id=id).values_list(
        "idobl__oblast", flat=True
    )


# Anja Mihajlov
# U bazu unosi novog korisnika koji je tipa O, tj. organizacija
def insertOrganization(ime, pib, telefon, email, lozinka) -> models.Korisnik:
    with transaction.atomic():
        organizacija = models.Korisnik(
            ime=ime, password=lozinka, email=email, pib=pib, telefon=telefon, tip="O"
        )
        organizacija.set_password(lozinka)
        organizacija.save()
    return organizacija


# Anja Mihajlov
# U bazu unosi novog korisnika tipa V, tj. volontera, radi insert u zanimaga
def insertVolunteer(ime, prezime, datumRodj, email, lozinka, cats) -> models.Korisnik:
    with transaction.atomic():
        volonter = models.Korisnik(
            ime       = ime,
            prezime   = prezime,
            datumrodj = datumRodj,
            password  = lozinka,
            email     = email,
            tip       = "V",
        )
        volonter.set_password(lozinka)
        volonter.save()
        for cat in cats:
            unos = models.ZanimaGa(idkor=volonter, idobl=getCategoryObject(cat))
            unos.save()
    return volonter


# Kosta Novokmet
# vraca sve aktivnosti kao listu
def getAllActivities() -> list[models.Aktivnost]:

    return list(models.Aktivnost.objects.all())


# Kosta Novokmet
# vraca sve prijave kao listu
def getAllApplications() -> list[models.Prijava]:

    return list(models.Prijava.objects.all())


# Kosta Novokmet
# vraca sve aktivnosti iz baze koje se nisu zavrsile za odredjenu organizaciju
def getActiveActivitiesOrg(korID) -> list:
    acts = getAllActivities()
    from . import utils

    return [
        act
        for act in acts
        if not utils.datePassed(act.datumdo) and act.idorg.idkor == korID
    ]


# Kosta Novokmet
# vraca sve aktivnosti iz baze koje su se zavrsile za odredjenu organizaciju
def getArchivedActivitiesOrg(korID) -> list:
    acts = getAllActivities()
    from . import utils

    return [
        act
        for act in acts
        if utils.datePassed(act.datumdo) and act.idorg.idkor == korID
    ]


# Kosta Novokmet
# vraca sve aktivnosti na kojima je volonter ucestvovao
def getActivitiesVol(korID) -> list[models.Aktivnost]:
    acts = getAllApplications()
    from . import utils

    return [
        act.idakt
        for act in acts
        if utils.datePassed(act.idakt.datumdo) and act.idvol.idkor == korID
    ]


# Kosta Novokmet
# vraca sve zahteve aktivnosti
def getActivityReqs(actID) -> list:
    return list(
        models.Vestina.objects.filter(idakt=actID).all().values_list("opis", flat=True)
    )


# Kosta Novokmet
# vraca sve prijave za odredjenu aktivnost u vidu liste recnika
# opciono se prosledi status prijava koje hocemo i da li je ta aktivnost prosla
# finished=True ako jeste i status='O/R/A'
# mora se proslediti idact=..
def getApplicationsForAct(**kwargs) -> list[dict]:
    app_status = kwargs.get("status", "O")
    passed = kwargs.get("finished", False)
    actID = kwargs["idakt"]
    apps = list(models.Prijava.objects.filter(idakt=actID, status=app_status).all())
    from . import utils

    if passed == True:
        return [
            {
                "preporukavol": app.preporukavol,
                "preporukaorg": app.preporukaorg,
                "komvol":       app.komvol,
                "komorg":       app.komorg,
                "status":       app.status,
                "idpri":        app.idpri,
                "idakt":        app.idakt.idakt,
                "idvol":        app.idvol.idkor,
                "volname":      app.idvol.ime,
                "vollastname":  app.idvol.prezime,
                "pismo":        app.pismo,
            }
            for app in apps
            if utils.datePassed(app.idakt.datumdo)
        ]

    else:
        return [
            {
                "preporukavol": app.preporukavol,
                "preporukaorg": app.preporukaorg,
                "komvol":       app.komvol,
                "komorg":       app.komorg,
                "status":       app.status,
                "idpri":        app.idpri,
                "idakt":        app.idakt.idakt,
                "idvol":        app.idvol.idkor,
                "volname":      app.idvol.ime,
                "vollastname":  app.idvol.prezime,
                "pismo":        app.pismo,
            }
            for app in apps
        ]


#Kosta Novokmet
#vraca sve aktivnosti na kojima je Korisnik prihvacen, ali tako da ta aktivnost nije pocela
def getAcceptedActs(user:models.Korisnik) -> list[models.Prijava]:
    apps = list(models.Prijava.objects.filter(idvol=user,status='A').all())
    acts = []
    from .utils import datePassed
    for app in apps:
        act = models.Aktivnost.objects.filter(idakt=app.idakt.idakt).first()
        if not datePassed(act.datumod):
            acts.append(act)
    return acts



# Kosta Novokmet
# vraca prijavu odredjenog volontera za odredjenu aktivnost kao recnik, ako nema vraca None
# opciono finished=True ako hocemo prijavu samo ako je ta akt prosla
# idakt i idkor moraju da se stave kao key val pair u pozivu fje
def getApplicationsForActVol(**kwargs) -> dict:
    passed = kwargs.get("finished", False)
    actID  = kwargs["idakt"]
    korID  = kwargs["idkor"]
    exists = kwargs.get("exists", False)
    if exists == True:
        return models.Prijava.objects.filter(idakt=actID, idvol=korID).exists()
    app = models.Prijava.objects.filter(idakt=actID, idvol=korID).first()
    if passed == True:
        from . import utils

        if app and utils.datePassed(app.idakt.datumdo):
            return {
                "preporukavol": app.preporukavol,
                "preporukaorg": app.preporukaorg,
                "komvol":       app.komvol,
                "komorg":       app.komorg,
                "status":       app.status,
                "idpri":        app.idpri,
                "idakt":        app.idakt.idakt,
                "idvol":        app.idvol.idkor,
                "volname":      app.idvol.ime,
                "vollastname":  app.idvol.prezime,
                "pismo":        app.pismo,
            }

        else:
            return None
    else:
        if app:
            return {
                "preporukavol": app.preporukavol,
                "preporukaorg": app.preporukaorg,
                "komvol":       app.komvol,
                "komorg":       app.komorg,
                "status":       app.status,
                "idpri":        app.idpri,
                "idakt":        app.idakt.idakt,
                "idvol":        app.idvol.idkor,
                "volname":      app.idvol.ime,
                "vollastname":  app.idvol.prezime,
                "pismo":        app.pismo,
            }
        else:
            return None


# Kosta Novokmet
# updatuje u bazi broj slob mesta za akktivnost actID na new_val
def updateFreeSpaces(new_val, actID) -> None:
    print(f"called with val{new_val} id{actID}")
    act = models.Aktivnost.objects.get(idakt=actID)
    act.brmesta = new_val
    act.save()


# Kosta Novokmet
# vraca user id ili user obj na osnovu email-a
def UsrFromEmail(**kwargs):
    target_email = kwargs["email"]
    id = kwargs.get("id", False)
    exists = kwargs.get("exists", False)
    if exists == True:
        return models.Korisnik.objects.filter(email=target_email).exists()
    usr = models.Korisnik.objects.filter(email=target_email).first()
    if id:
        return usr.idkor
    else:
        return usr


# Kosta Novokmet
# vraca usera na osnovu pib-a
def UsrFromPib(**kwargs):
    target_pib = kwargs["pib"]
    exists = kwargs.get("exists", False)
    if exists == True:
        return models.Korisnik.objects.filter(pib=target_pib).exists()
    usr = models.Korisnik.objects.filter(pib=target_pib).first()
    return usr


# Kosta Novokmet
# vraca usera na osnovu pib-a
def UsrFromTel(**kwargs):
    target_tel = kwargs["tel"]
    exists = kwargs.get("exists", False)
    if exists == True:
        return models.Korisnik.objects.filter(telefon=target_tel).exists()
    usr = models.Korisnik.objects.filter(telefon=target_tel).first()
    return usr


def getApplicationById(idPri) -> models.Prijava:
    return models.Prijava.objects.filter(idpri=idPri).first()


# Kosta Novokmet
def getActivityById(idAkt) -> models.Aktivnost:
    return models.Aktivnost.objects.filter(idakt=idAkt).first()


# Kosta Novokmet
def getUsrById(id) -> models.Korisnik:
    return models.Korisnik.objects.filter(idkor=id).first()


def insertApplication(idvol, idakt, pismo, rezimeFile) -> models.Prijava:
    with transaction.atomic():
        prijava = models.Prijava(
            idvol  = idvol,
            idakt  = getActivityById(idAkt=idakt),
            pismo  = pismo,
            rezime = rezimeFile.file.read() if rezimeFile is not None else None,
            status = "O",
        )
        prijava.save()
    return prijava


# Kosta Novokmet
def getChats(id) -> list[models.Prepiska]:
    from django.db.models import Q

    return list(models.Prepiska.objects.filter(Q(idkor1=id) | Q(idkor2=id)).all())


def insertChat(id1, id2) -> models.Prepiska:
    kor1 = getUsrById(id1)
    kor2 = getUsrById(id2)
    if models.Prepiska.objects.filter(idkor1=id1, idkor2=id2).exists():
        return
    if models.Prepiska.objects.filter(idkor2=id1, idkor1=id2).exists():
        return
    with transaction.atomic():
        chat = models.Prepiska(idkor1=kor1, idkor2=kor2)
        print("chat saved")
        chat.save()
        from datetime import datetime, timezone

        sender = getUsrById(id1)
        msg = models.Poruka(
            idpre    = chat,
            status   = "U",
            time     = datetime.now(timezone.utc),
            tekst    = f"Korisnik {sender.ime} je zapoceo prepisku",
            redbr    = 1,
            idsender = sender,
        )
        msg.save()
    return chat


def getMessages(chat_id, id_reader):
    messages = list(models.Poruka.objects.filter(idpre=chat_id).all())
    for message in messages:
        if message.idsender_id != id_reader:
            message.status = "R"
            message.save()
    return messages


# Natalija Vujnic
# azurira profil korisnika tipa organizacija
def editOrganization(korisnik, newIme, newPib, newTel) -> None:
    with transaction.atomic():
        korisnik.ime = newIme
        korisnik.pib = newPib
        korisnik.telefon = newTel
        korisnik.save()


# Natalija Vujnic
# azurira profil korisnika tipa volonter
def editVolunteer(korisnik, newIme, newPrezime, newDatum, newCats) -> None:
    with transaction.atomic():
        korisnik.ime = newIme
        korisnik.prezime = newPrezime
        korisnik.datumrodj = newDatum
        korisnik.save()
        models.ZanimaGa.objects.filter(idkor_id=korisnik.idkor).delete()
        for cat in newCats:
            category = getCategoryById(cat)
            if category is not None:
                unos = models.ZanimaGa(idkor=korisnik, idobl=category)
                unos.save()


# Natalija Vujnic
# vraca listu svih interesovanja
def getAllInteresIds() -> list:
    return models.Oblast.objects.all()


# Natalija Vujnic
# vraca listu interesovanja za konkretnog korisnika
def getInterestsIds(id) -> list:
    return models.ZanimaGa.objects.filter(idkor_id=id).values_list("idobl", flat=True)


# Natalija Vujnic
# vraca kategoriju na osnovu identifikatora
def getCategoryById(id) -> models.Oblast:
    return models.Oblast.objects.filter(idobl=id).first()


# Anja Mihajlov
# Dohvata sve organizacije iz baze
def getAllOrganizations() -> list:
    return list(models.Korisnik.objects.filter(tip="O"))


# Anja Mihajlov
# Filtrira organizacije na osnovu imena
def filterOrganizationsName(name) -> list:
    return list(models.Korisnik.objects.filter(tip="O", ime__icontains=name))


# Anja Mihajlov
# Dohvata sve volontere iz baze
def getAllVolunteers():
    return models.Korisnik.objects.filter(tip="V")


# Anja Mihajlov
# Filtrira volontere na osnovu imena
def filterVolunteersName(name, vols):
    from django.db.models import Q

    return vols.filter(Q(ime__istartswith=name) | Q(prezime__istartswith=name))


# Anja Mihajlov
# filtrira volontere na osnovu iskustva
def filterVolunteerExperience(exp, vols):
    from datetime import date

    today = date.today()

    active_volunteers = models.Prijava.objects.filter(
        status="A", idakt__datumdo__lt=today
    ).select_related("idvol")

    vol_ids = [p.idvol for p in active_volunteers]
    if exp:
        filtered_vols = [vol for vol in vols if vol in vol_ids]
    else:
        filtered_vols = [vol for vol in vols if vol not in vol_ids]

    return filtered_vols


# Anja Mihajlov
# Filtrira volontera na osnovu interesovanja
def filterVolunteerCategories(vols, cats):
    vol_ids = list(
        models.ZanimaGa.objects.filter(idobl__in=cats).values_list("idkor", flat=True)
    )
    return [vol for vol in vols if vol.idkor in vol_ids]


# Natalija Vujnic
# vraca listu volontera koji su ucestvovali na konkretnoj aktivnosti, a nisu jos uvek ocenjeni
def getUnreviewedApplications(idAkt) -> list:
    return models.Prijava.objects.filter(idakt=idAkt).filter(preporukaorg__isnull=True)


# Natalija Vujnic
# dohvata korisnika na osnovu mejla
def getUserEmail(id):
    return models.Korisnik.objects.filter(email=id).first()


# Natalija Vujnic
# unosi komentar od organizacije za konkretnu prijavu
def writeCommentOrg(idPrijave, ocena, komentar):
    with transaction.atomic():
        rows_updated = models.Prijava.objects.filter(idpri=idPrijave).update(
            preporukaorg=ocena, komorg=komentar
        )


# Natalija Vujnic
# Vraca listu organizacija na cijim arhiviranim aktivnostima je ucestvovao volonter, a da nisu jos uvek ocenjene
def getUnreviewedOrgs(idVol) -> list:
    return models.Prijava.objects.filter(
        idvol=idVol,
        status="A",
    ).filter(preporukavol__isnull=True)


# Natalija Vujnic
# unosi komentar od volontera za konkretnu prijavu
def writeCommentVol(idPrijave, ocena, komentar):
    with transaction.atomic():
        rows_updated = models.Prijava.objects.filter(idpri=idPrijave).update(
            preporukavol=ocena, komvol=komentar
        )


# Anja Mihajlov
# Dohvata oblasti kojima aktivnost pripada
def getCategorisForActivity(idAkt):
    return models.Oblast.objects.filter(aktivnosti__idakt=idAkt)


# Anja Mihajlov
# Dohvata vestine potrebne za neku aktivnost
def getSkillsForActivity(idAkt):
    return models.Vestina.objects.filter(idakt=idAkt)


# Anja Mihajlov
# Dohvata sve otvorene aktivnosti za koje ima sobodnih mesta
def getActiveActivities():
    from datetime import date

    today = date.today()
    all_activities = models.Aktivnost.objects.all()
    active_activities = all_activities.exclude(datumrok__lt=today)
    active_activities = active_activities.exclude(brmesta__lt=1)
    return active_activities


# Anja Mihajlov
# Filtrirane aktivnosti nakon nekog datuma
def getActivitiesAfter(acts, datumod):
    from datetime import datetime

    datumod = datetime.strptime(datumod, "%Y-%m-%d").date()
    return acts.exclude(datumod__lte=datumod)


# Anja Mihajlov
# Filtrirane aktivnosti do nekog datuma
def getActivitiesBefore(acts, datumdo):
    from datetime import datetime

    datumdo = datetime.strptime(datumdo, "%Y-%m-%d").date()
    return acts.exclude(datumdo__gte=datumdo)


# Anja Mihajlov
# Dohvata sve postojece potrebne vestine
def getAllSkills():
    return list(models.Vestina.objects.all())


# Anja Mihajlov
# Dohvata sva postejaca interesovanja
def getAllCats():
    return list(models.Oblast.objects.all())


"""
#Anja Mihajlov
#Filtrira aktivnosti na osnovu skillova
def filterActBySkills(acts, skills):
from django.db.models import Q
skills_set = set(map(int, skills))
matching_activity_ids = []
for act in acts:
    activity_skills = models.Vestina.objects.filter(idakt=act.idakt).values_list('idves', flat=True)
    activity_skills_set = set(activity_skills)
    if skills_set.issuperset(activity_skills_set):
        matching_activity_ids.append(act.idakt)
filtered_activities = acts.filter(Q(idakt__in=matching_activity_ids))
return filtered_activities
"""


# Anja Mihajlov
# Filtrira aktivnosti na osnovu oblasti
def filterActsByCat(acts, area):
    matching_activity_ids = models.Pripada.objects.filter(idobl=area).values_list(
        "idakt", flat=True
    )
    filtered_activities = acts.filter(idakt__in=matching_activity_ids)
    return filtered_activities


# Anja Mihajlov
# Filtrira aktivnosti na osnovu oblasti
def getActivitiesContinent(acts, kontinent):
    lokacije = models.Lokacija.objects.filter(kontinent=kontinent).values_list(
        "idlok", flat=True
    )
    print(lokacije)
    filtered_activities = acts.filter(lokacija__in=lokacije)
    return filtered_activities


#Anja Mihajlov
#Brisanje aktivnosti
def deleteAktivnost(IdAktivnost):
    from django.core.exceptions import ObjectDoesNotExist
    with transaction.atomic():
        try:
            aktivnost = models.Aktivnost.objects.get(idakt=IdAktivnost)
            if(aktivnost):
                aktivnost.delete()
                return "Obrisana aktivnost " + IdAktivnost
        except ObjectDoesNotExist:
            return "Ne postoji aktivnost sa tim ID"


#Anja Mihajlov
#Brisanje aktivnosti
def deleteUser(email):
    from django.core.exceptions import ObjectDoesNotExist
    with transaction.atomic():
        try:
            user = models.Korisnik.objects.get(email=email)
            if user:
                user.delete()
                return "Obrisan korisnik " + email
        except ObjectDoesNotExist:
            return "Ne postoji korisnik sa tom email adresom"
        

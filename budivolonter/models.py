from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Aktivnost(models.Model):
    idorg    = models.ForeignKey('Korisnik', models.DO_NOTHING, db_column='idOrg')  # Field name made lowercase.
    idakt    = models.AutoField(db_column='idAkt', primary_key=True)  # Field name made lowercase.
    naziv    = models.CharField(max_length=255)
    brmesta  = models.IntegerField(db_column='brMesta')  # Field name made lowercase.
    datumod  = models.DateField(db_column='datumOd')  # Field name made lowercase.
    datumdo  = models.DateField(db_column='datumDo')  # Field name made lowercase.
    datumrok = models.DateField(db_column='datumRok')  # Field name made lowercase.
    mesto    = models.CharField(max_length=255)
    lokacija = models.ForeignKey('Lokacija', models.DO_NOTHING, db_column='lokacija')
    opis     = models.CharField(max_length=3000, blank=True, null=True)
    oblasti  = models.ManyToManyField('Oblast',through='Pripada')

    class Meta:
        managed = True
        db_table = 'aktivnost'


class Korisnik(AbstractBaseUser):
    idkor     = models.AutoField(db_column='idKor', primary_key=True)  # Field name made lowercase.
    email     = models.CharField(unique=True, max_length=255)
    password  = models.CharField(max_length=255)
    ime       = models.CharField(max_length=255)
    prezime   = models.CharField(max_length=255, blank=True, null=True)
    pib       = models.IntegerField(unique=True, blank=True, null=True)
    telefon   = models.CharField(unique=True, max_length=14, blank=True, null=True)
    tip       = models.CharField(max_length=1)
    datumrodj = models.DateField(db_column='datumRodj', blank=True, null=True)  # Field name made lowercase.
    oblasti   = models.ManyToManyField('Oblast',through='ZanimaGa')

    class Meta:
        managed  = True
        db_table = 'korisnik'

    USERNAME_FIELD = 'email'
    EMAIL_FIELD    = 'email'


class Lokacija(models.Model):
    drzava    = models.CharField(max_length=256)
    kontinent = models.CharField(max_length=256)
    idlok     = models.AutoField(db_column='idLok', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'lokacija'


class Oblast(models.Model):
    oblast     = models.CharField(max_length=256)
    idobl      = models.AutoField(db_column='idObl', primary_key=True)  # Field name made lowercase.
    aktivnosti = models.ManyToManyField(Aktivnost,through='Pripada')
    korisnici  = models.ManyToManyField(Korisnik,through='ZanimaGa')


    class Meta:
        managed = True
        db_table = 'oblast'


class Poruka(models.Model):
    idpor    = models.AutoField(db_column='idPor', primary_key=True)
    idpre    = models.ForeignKey('Prepiska', models.DO_NOTHING, db_column='idPre')  # Field name made lowercase. The composite primary key (idPre, redBr) found, that is not supported. The first column is selected.
    redbr    = models.CharField(db_column='redBr', max_length=45)  # Field name made lowercase.
    tekst    = models.CharField(max_length=2000)
    time     = models.DateTimeField()
    status   = models.CharField(max_length=1)
    idsender = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='idSender')  # Field name made lowercase.

    class Meta:
        managed         = True
        db_table        = 'poruka'
        unique_together = (('idpre', 'redbr'),)


class Prepiska(models.Model):
    idpre  = models.AutoField(db_column='idPre', primary_key=True)  # Field name made lowercase.
    idkor1 = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='idKor1')  # Field name made lowercase.
    idkor2 = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='idKor2', related_name='prepiska_idkor2_set')  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'prepiska'


class Prijava(models.Model):
    idpri        = models.AutoField(db_column='idPri', primary_key=True)  # Field name made lowercase.
    idvol        = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='idVol')  # Field name made lowercase.
    idakt        = models.ForeignKey(Aktivnost, models.DO_NOTHING, db_column='idAkt')  # Field name made lowercase.
    pismo        = models.CharField(max_length=2000)
    rezime       = models.BinaryField(blank=True, null=True)
    status       = models.CharField(max_length=1)
    preporukavol = models.CharField(db_column='preporukaVol', max_length=1, blank=True, null=True)  # Field name made lowercase.
    preporukaorg = models.CharField(db_column='preporukaOrg', max_length=1, blank=True, null=True)  # Field name made lowercase.
    komvol       = models.CharField(db_column='komVol', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    komorg       = models.CharField(db_column='komOrg', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'prijava'


class Pripada(models.Model):
    idobl = models.ForeignKey(Oblast,on_delete=models.CASCADE, db_column='idObl')  # Field name made lowercase.
    idakt = models.ForeignKey(Aktivnost,on_delete=models.CASCADE, db_column='idAkt')
    class Meta:
        managed         = True 
        db_table        = 'pripada'
        unique_together = (('idakt', 'idobl'),)


class Vestina(models.Model):
    idakt = models.ForeignKey(Aktivnost, models.DO_NOTHING, db_column='idAkt')  # Field name made lowercase.
    idves = models.AutoField(db_column='idVes', primary_key=True)  # Field name made lowercase.
    opis  = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 'vestina'


class ZanimaGa(models.Model):
    idkor = models.ForeignKey(Korisnik,on_delete=models.CASCADE, db_column='idKor')
    idobl = models.ForeignKey(Oblast,on_delete=models.CASCADE, db_column='idObl')  # Field name made lowercase.
    class Meta:
        managed         = True 
        db_table        = 'zanima_ga'
        unique_together = (('idkor', 'idobl'),)

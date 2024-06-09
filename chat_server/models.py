from django.db import models


class Korisnik(models.Model):
    idkor         = models.AutoField(
        db_column = "idKor", primary_key=True
    )  # Field name made lowercase.
    email         = models.CharField(unique=True, max_length=255)
    password      = models.CharField(max_length=255)
    ime           = models.CharField(max_length=255)
    prezime       = models.CharField(max_length=255, blank=True, null=True)
    pib           = models.IntegerField(unique=True, blank=True, null=True)
    telefon       = models.CharField(unique=True, max_length=14, blank=True, null=True)
    tip           = models.CharField(max_length=1)
    datumrodj     = models.DateField(
        db_column = "datumRodj", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "korisnik"


class Poruka(models.Model):
    idpor    = models.AutoField(db_column = "idPor", primary_key = True)
    idpre    = models.ForeignKey("Prepiska", models.DO_NOTHING, db_column = "idPre")  # Field name made lowercase. The composite primary key (idPre, redBr) found, that is not supported. The first column is selected.
    redbr    = models.CharField(db_column = "redBr", max_length=45)  # Field name made lowercase.
    tekst    = models.CharField(max_length = 2000)
    time     = models.DateTimeField()
    status   = models.CharField(max_length = 1)
    idsender = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column = "idSender")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "poruka"
        unique_together = (("idpre", "redbr"),)


class Prepiska(models.Model):
    idpre = models.AutoField(
        db_column="idPre", primary_key=True
    )  # Field name made lowercase.
    idkor1 = models.ForeignKey(
        Korisnik, models.DO_NOTHING, db_column="idKor1"
    )  # Field name made lowercase.
    idkor2 = models.ForeignKey(
        Korisnik,
        models.DO_NOTHING,
        db_column="idKor2",
        related_name="prepiska_idkor2_set",
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "prepiska"

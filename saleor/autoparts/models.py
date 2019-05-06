from django.db import models
from django.db.models import Model


class Automaker(Model):
    brand = models.CharField(max_length=128)
    ttc_mfa_id_old = models.TextField(blank=True)
    ttc_mfa_id_new = models.TextField(blank=True)
    logo_picture = models.TextField(blank=True)
    from_year = models.TextField(blank=True)
    to_year = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        app_label = 'autoparts'
        ordering = ('brand',)

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.brand)

    def __str__(self):
        return self.brand


class Series(Model):
    name = models.CharField(max_length=128)
    logo_picture = models.TextField(blank=True)
    automaker = models.ForeignKey(
        Automaker, related_name='series', on_delete=models.CASCADE)


class CarModel(Model):
    model_car = models.TextField(blank=True)
    ttc_mod_id = models.TextField(blank=True)
    logo_picture = models.TextField(blank=True)
    series = models.ForeignKey(
        Series, related_name='models', on_delete=models.CASCADE)


class Modification(Model):
    type_car = models.TextField(blank=True)  # TYP_CAR - type car (engine data) ***
    body_type = models.TextField(blank=True)  # BODY_TYPE - body type ***
    of_the_year = models.DateTimeField(null=True)  # OF_THE_YEAR - from year for type car
    up_to_year = models.DateTimeField(null=True)  # UP_TO_A_YEAR - to year for type car
    kw = models.TextField(blank=True)  # KW - kw
    hp = models.TextField(blank=True)  # PM - pm/hp
    engine_cc = models.TextField(blank=True, null=True)  # CC - ccm
    ttc_typ_id = models.TextField(blank=True, primary_key=True, unique=True)
    technical_information = models.TextField(blank=True)  # technical info of car (list characteristics of car) ***
    engine_codes = models.TextField(blank=True)  # list code engines
    car_model = models.ForeignKey(
        CarModel, related_name='modifications', on_delete=models.CASCADE)


class PartBrand(Model):
    name = models.TextField()
    logo_picture = models.TextField(blank=True)

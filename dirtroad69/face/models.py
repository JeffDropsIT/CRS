from django.db import models
from django.core.urlresolvers import reverse



class Cow(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    JERSEY = 'Jersey'
    AUBRAC = 'Aubrac'
    T1 = 'Horned In Both Sexes'
    T2 = 'Male Only Horned '
    HORN_CHOICES = (
        (T1, 'Horned In Both Sexes'),
        (T2, 'Male Only Horned '),
        )
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
        default=FEMALE)
    BREED_CHOICES = (
        (JERSEY, 'Jersey'),
        (AUBRAC, 'Aubrac'),
        )
    breed = models.CharField(max_length=15, choices=BREED_CHOICES,
        default=JERSEY)
    coat_color = models.CharField(max_length=100, default=None)

    horn_status = models.CharField(max_length=50, choices=HORN_CHOICES,
        default=T1)

    used_for = models.CharField(max_length=100, default=None)
    cow_img = models.FileField(default=None)

    def get_absolute_url(self):
        return reverse('face:detail', kwargs={'pk':self.pk})

    def is_upperclass(self):
        return self.gender in (self.MALE, self.FEMALE)

    def __str__(self):
        return self.name +" - "+" "+self.breed


class Cattle_Retrain(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    cow_video_1 = models.FileField(default=None)
    cow_video_2 = models.FileField(default=None)
    cow_video_3 = models.FileField(default=None)
    cow_video_4 = models.FileField(default=None)

   # def get_absolute_url(self):
     #   return reverse('face:retrain', kwargs={'pk':self.pk})

class CattleLog(models.Model):
    NO = 'NO'
    YES = 'YES'
    A = ' 1-10 pts '
    B = '10-20 pts'
    C = '20-30 pts'
    D = '30-40 pts'
    E = '50-60 pts'
    F = '60-70 pts'
    G = '70-80 pts'
    H = '80-90 pts'
    I = '90-100 pts'
    LAC_CHOICES = (
        (NO, 'NO'),
        (YES, 'YES'),
    )
    PTS_CHOICES = (
        (A, ' 1-10 pts'),
        (B, '10-20 pts'),
        (C, '20-30 pts'),
        (D, '30-40 pts'),
        (E, '50-60 pts'),
        (F, '60-70 pts'),
        (G, '70-80 pts'),
        (G, '70-80 pts'),
        (H, '80-90 pts'),
        (I, '90-100 pts'),
    )
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    log = models.DateTimeField()
    birth_date = models.DateField()  # this must go in the cow model as it is a constant
    description = models.CharField(max_length=100000)

    lactating = models.CharField(max_length=15, choices=LAC_CHOICES,
        default=NO)
    feeding_scheme = models.CharField(max_length=100)
    condition_score = models.CharField(max_length=15, choices=PTS_CHOICES,
        default=A)
    injection_type = models.CharField(max_length=100)
    weight = models.PositiveSmallIntegerField(default=0)
    injection_Last_Date = models.DateTimeField()
    insemination_date = models.DateTimeField()

    def __str__(self):
        return 'last log date: '+str(self.log)


class CattleImage(models.Model):
    classify_img = models.FileField(default=None)
    def get_absolute_url(self):
        return reverse('face:detail', kwargs={'pk':self.pk})
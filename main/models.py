from django.db import models

# Create your models here.
class RFK(models.Model):
    version = models.CharField(max_length=6) # 'version': 'ICFEN2',
    Dimension = models.CharField(max_length=1) # 'Dimension': 'b',
    Chapter = models.CharField(max_length=1) # 'Chapter': '1',
    Block = models.CharField(max_length=1) # 'Block': '0',
    SecondLevel = models.CharField(max_length=2) # 'SecondLevel': '0',
    ThirdLevel = models.CharField(max_length=1) # 'ThirdLevel': '0',
    FourthLevel = models.CharField(max_length=1) # 'FourthLevel': '0',
    levelno = models.SmallIntegerField() # 'levelno': '2',
    code = models.CharField(max_length=9) # 'code': 'b1',
    parent = models.CharField(max_length=5) # 'parent': 'b',
    mlsort = models.SmallIntegerField() # 'mlsort': '1',
    leafnode = models.SmallIntegerField() # 'leafnode': '0',
    Title = models.TextField() # 'Title': 'MENTAL FUNCTIONS',
    Description = models.TextField() # 'Description': 'This chapter ...',
    Inclusions = models.TextField() # 'Inclusions': '',
    Exclusions = models.TextField() # 'Exclusions': '',
    selected = models.CharField(max_length=1) # 'selected': '1',
    Translated_title = models.TextField() # 'Translated_title': 'VAIMSED FUNKTSIOONID',
    Translated_description = models.TextField() # 'Translated_description': 'See peatükk käsitleb ...',
    Translated_inclusions = models.TextField() # 'Translated_inclusions': '',
    Translated_exclusions = models.TextField() # 'Translated_exclusions': ''

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code

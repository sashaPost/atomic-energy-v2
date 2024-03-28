from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Unit(models.Model):
    ua_name = models.CharField(max_length=255, unique=True)
    en_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.ua_name
    
class Procurement(models.Model):
    tender_id = models.CharField(max_length=255, verbose_name='Tender ID')    # tenderID 
    title = models.CharField(max_length=255, verbose_name='Title')    # title
    product_code = models.CharField(max_length=50, verbose_name='Product Code')
    purchase_code = models.CharField(max_length=50, verbose_name='Purchase Code')        
    prozorro_id = models.CharField(max_length=50, unique=True, verbose_name='ProZorro ID')    # id
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='Unit')
    date = models.DateField(db_index=True, verbose_name='Tender Date')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Added By')
    date_added = models.DateTimeField(auto_now_add=True)
    visibility = models.BooleanField(default=False, verbose_name='Visibility')
    file = models.FileField(upload_to='files/', verbose_name='File Field')
    
    def __str__(self):
        return self.prozorro_id
    
class ProcuringEntity(models.Model):
    # procuringEntity (add 'blank=True')
    procurement = models.OneToOneField(Procurement, on_delete=models.CASCADE, related_name='procuring_entity')
    identifier_id = models.CharField(max_length=8, null=True)    # identifier->id
    identifier_scheme = models.CharField(max_length=10, null=True)    # identifier->scheme
    identifier_name = models.CharField(max_length=255, null=True)    # name
    country_name = models.CharField(max_length=32, null=True)    #address->countryName
    postal_code = models.CharField(max_length=5, null=True)    # address->postalCode
    region = models.CharField(max_length=32, null=True)    # address->region  
    locality = models.CharField(max_length=32, null=True)    # address->locality
    address = models.CharField(max_length=255, null=True)    # address->streetAddress
    contact_email = models.CharField(max_length=62, null=True)    # contactPoint->email 
    contact_phone = models.CharField(max_length=12, null=True)    # contactPoint->telephone
    contact_url = models.CharField(max_length=255, null=True)    # contactPoint->url
    contact_name = models.CharField(max_length=255, null=True)    # contactPoint->name
    
    def __str__(self):
        return self.id
    
class Value(models.Model):
    # value
    procurement = models.OneToOneField(Procurement, on_delete=models.CASCADE, related_name='value')
    amount = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    currency = models.CharField(max_length=3, null=True)
    
    def __str__(self):
        return self.id
    
class Item(models.Model):
    procurement = models.ForeignKey(Procurement, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255, null=True)
    classification_id = models.CharField(max_length=10, null=True)
    classification_scheme = models.CharField(max_length=10, null=True)
    classification_description = models.CharField(max_length=255, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unit_name = models.CharField(max_length=255, null=True)    # unit->name
    delivery_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.id
        
class TenderPeriod(models.Model):
    procurement = models.OneToOneField(Procurement, on_delete=models.CASCADE, related_name='periods')    
    start_date = models.DateTimeField(null=True)    # tenderPeriod->startDate
    start_date = models.DateTimeField(null=True)    # tenderPeriod->endDate
    
    def __str__(self):
        return self.id
        
class TenderStep(models.Model):
    procurement = models.OneToOneField(Procurement, on_delete=models.CASCADE, related_name='step')
    currency = models.CharField(max_length=3, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    
    def __str__(self):
        return self.id
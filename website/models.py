from django.db import models
from django.forms import ModelForm

class Item(models.Model):
    name = models.CharField(max_length=100) 
    quantity = models.IntegerField(default=0)  
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Item_form(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'weight']
        

from django.db import models

# Create your models here.
class SalesData(models.Model):
    date = models.DateField()
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"{self.date} - {self.sales}"
    
    class Meta:
        db_table = 'sales_data'    

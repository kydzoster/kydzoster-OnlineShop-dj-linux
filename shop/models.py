from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    # will create unique indexes
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    # foreign key to category model, with one-to-many relationship. 
    # Meaning, product belongs to one category and a category contains multiple products
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # Name of the Product
    name = models.CharField(max_length=200, db_index=True)
    # URL
    slug = models.SlugField(max_length=200, db_index=True)
    # Optional product image
    image = models.ImageField(upload_to='products/%d/%m/%Y', blank=True)
    # optional description
    description = models.TextField(blank=True)
    # Stores decimal numbers with max 10 digits. Decimal field is better used with currency.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Boolean value indicates if product is available or not. Enable/Disable product in category
    available = models.BooleanField(default=True)
    # when object was created
    created = models.DateTimeField(auto_now_add=True)
    # when object was last updated
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        # id and slug are indexed together for query purposes
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

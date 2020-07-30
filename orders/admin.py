import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# httpresponse has to be treated as CSV file
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    # httpresponse contains an attached file
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    # csv writer will write to the response object
    writer = csv.writer(response)
    # excludes many-to-many and one-to-many relationships
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write a header row including the field names
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows for each object returned by the queryset
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'

# takes order object as an argument and returns an HTML link
def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    # use mark_safe to avoid auto escaping, 
    # avoid using mark_safe on input that has come from the user to avoid XSS threats
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    # inline allows to include a model on the same edit page as its related model
    inlines = [OrderItemInline]
    actions = [export_to_csv]

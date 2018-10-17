from django.contrib import admin

# Register your models here.
from collection.models import Results



#set up automated slug creation
class ResultsAdmin(admin.ModelAdmin):
    model = Results
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}

#registering Results model
admin.site.register(Results, ResultsAdmin)

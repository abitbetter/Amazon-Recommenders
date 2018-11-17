from django.contrib import admin

# Register your models here.
from collection.models import Results
from collection.modelsfile import Books
from collection.modelsfile import Movies
from collection.dbrouter import MultiDBModelAdmin

#set up automated slug creation
class ResultsAdmin(admin.ModelAdmin):
    model = Results
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}

# class BooksAdmin(admin.ModelAdmin):
#     #don't think i need this?
#     #using = 'reviews'
#     def get_queryset(self, request):
#         # Tell Django to look for objects on the 'other' database.
#         return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

#registering Results model
admin.site.register(Results, ResultsAdmin)

admin.site.register(Books, MultiDBModelAdmin)

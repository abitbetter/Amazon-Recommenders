from django.shortcuts import render
from collection.models import Results
from collection.modelsfile import Books
from collection.modelsfile import Movies
from django_tables2 import RequestConfig
from collection.tables import ResultsTable

from django.views.generic import TemplateView
from collection.forms import HomeForm
from collection.dbrouter import MultiDBModelAdmin
from collection.Unpickle import unpickle, get_index_from_name, print_similar_books, open_data, wrangled_data

# Create your views here.
def index(request):
	results = Results.objects.all().order_by('name')
	return render(request, 'index.html', {
		'results' : results,
	})

class ResultsView(TemplateView):
	template_name = "results.html"

	def get(self, request):
		template_name = 'results.html'
		form = HomeForm(request.GET)
		if form.is_valid():
			form.save()
			input = form.cleaned_data['post']
			df = open_data(wrangled_data)
			if request.GET.get('knn'):
				model_type = 'K Nearest Neighbors'
				model = unpickle()
				results = print_similar_books(df, query=input, model=model)
				#results = {'1': 'Abraham Lincoln: Vampire Hunter', '2': "There's No Place Like Space: All About Our Solar System (Cat in the Hat's Learning Library)", '3': 'And When She Was Good: A Novel', '4': "George Washington's Secret Six: The Spy Ring That Saved the American Revolution"}

			args = {'results': results, 'input': input, 'model_type': model_type}
		return render(request, template_name, args)

def result_detail(request, slug):
	#grab the object
	result=Results.objects.get(slug=slug)
	#and pass to the template
	return render(request, 'results/result_detail.html', {
		'result': result,
	})

class HomeView(TemplateView):
	template_name = 'base.html'
	def get(self,request):
		form = HomeForm()
		return render(request, self.template_name, {'form': form})

from django.shortcuts import render
from collection.models import Results
from collection.modelsfile import Books
from collection.modelsfile import Movies
from django_tables2 import RequestConfig
from collection.tables import ResultsTable

from django.views.generic import TemplateView
from collection.forms import HomeForm
from collection.dbrouter import MultiDBModelAdmin
#from collection.Unpickle import unpickle, get_index_from_name, print_similar_books, open_data, wrangled_data

class ResultsView(TemplateView):
	template_name = "results.html"

	def get(self, request):
		template_name = 'results.html'
		form = HomeForm(request.GET)
		if form.is_valid():
			form.save()
			input = form.cleaned_data['post']
			#df = open_data(wrangled_data)
			if request.GET.get('knn'):
				model_type = 'K Nearest Neighbors'
				model = unpickle()
				results = print_similar_books(df, query=input, model=model)
				#results = {'Abraham Lincoln: Vampire Hunter', "There's No Place Like Space: All About Our Solar System (Cat in the Hat's Learning Library)", 'And When She Was Good: A Novel', "George Washington's Secret Six: The Spy Ring That Saved the American Revolution"}
			elif request.GET.get('svd'):
				model_type = 'Singular Value Decomposition'
				corr = unpickle_corr()
				book_title = unpickle_titles()
				results = print_recs(book_title, corr, input)
			elif request.GET.get('nmf'):
				model_type = 'Non-negative Matrix Factorization'
				item_item_dist = unpickle_matrix()
				dict = unpickle_dict()
				results = item_item_recommendation(item_emdedding_distance_matrix = item_item_dist,
				                                    item_id = input,
				                                    item_dict = dict,
				                                    n_items = 5, show=False)
			args = {'results': results, 'input': input, 'model_type': model_type}
		return render(request, template_name, args)

class HomeView(TemplateView):
	template_name = 'base.html'
	def get(self,request):
		form = HomeForm()
		return render(request, self.template_name, {'form': form})

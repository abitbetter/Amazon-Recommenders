from django.shortcuts import render
from collection.models import Results
from collection.modelsfile import Books
from collection.modelsfile import Movies

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
				model = unpickle()
				results = print_similar_books(df, query=input, model=model)

			#results = Books.objects.only("product_title").filter(index=input).using('reviews')
			args = {'results': results}
		return render(request, template_name, args)

def result_detail(request, slug):
	#grab the object
	result=Results.objects.get(slug=slug)
	#and pass to the template
	return render(request, 'results/result_detail.html', {
		'result': result,
	})

# def getResults(request, input):
# 	template_name = 'results.html'
# 	#unpickle knn models
# 	#clf = unpickle()
# 	#results = print_similar_books()
# 	results = Books.objects.only("product_title").filter(index=input).using('reviews')
# 	args = {'results': results}
# 	return render(request, template_name, args )

class HomeView(TemplateView):
	template_name = 'base.html'
	def get(self,request):
		form = HomeForm()
		return render(request, self.template_name, {'form': form})

	def post(self,request):
		if request.method == "POST":
			template_name = 'results.html'
			form = HomeForm(request.POST)
			if form.is_valid():
				form.save()
				#book title input
				input = form.cleaned_data['post']
				#model type to run
				#selection = form.cleaned_data['model_type']

				#unpickle KNN model
				# clf = unpickle()
				# if request.POST.get('knnbutton'):
				# 	results = print_similar_books()
				# elif request.POST.get('svdbutton'):
				# 	# results = predictSVD()
				# elif request.POST.get('otherbutton'):
				# 	# results = predictOther()

				results = Books.objects.only("product_title").filter(index=input).using('reviews')
				for result in results:
					print(result.product_title)
			form = HomeForm()
			args = {'form': form, 'results': results}
			return render(request, self.template_name, args)

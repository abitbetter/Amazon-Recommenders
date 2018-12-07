from django.shortcuts import render
from collection.models import Results
from collection.modelsfile import Books
from collection.modelsfile import Movies

from django.views.generic import TemplateView
from collection.forms import HomeForm
from collection.dbrouter import MultiDBModelAdmin
from collection.Unpickle import unpickle, get_index_from_name, print_similar_books

# Create your views here.
def index(request):
	results = Results.objects.all().order_by('name')
	return render(request, 'index.html', {
		'results' : results,
	})

def results(request):
	return render(request,'results.html')

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

	def post(self,request):
		form = HomeForm(request.POST)
		if form.is_valid():
			form.save()
			#book title input
			input = form.cleaned_data['post']
			#model type to run
			selection = form.cleaned_data['model_type']
			#unpickle KNN model
			clf = unpickle()
			print(clf.type())
			recommendations = print_similar_books()
			#text = get_queryset(Books.objects.only("product_title").value.filter(index=input).using('reviews'))
			titles = Books.objects.only("product_id").filter(product_title=input).using('reviews')
		form = HomeForm()
		args = {'form': form, 'titles': titles}
		return render(request, self.template_name, args)

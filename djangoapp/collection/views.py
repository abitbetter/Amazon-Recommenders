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

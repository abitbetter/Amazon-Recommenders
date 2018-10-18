from django.shortcuts import render
from collection.models import Results

from django.views.generic import TemplateView
from collection.forms import HomeForm

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
			text = form.cleaned_data('post')
		args = {'form': form, 'text': text}
		return render(request, self.template_name, args)

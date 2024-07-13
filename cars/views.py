from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import Carform,CarModelForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from django.views.generic import ListView,CreateView, DetailView, UpdateView, DeleteView



def cars_view(request):
    cars = Car.objects.all()
    search = request.GET.get('search')

    if search:
      cars = Car.objects.filter(model__icontains=search) # Buaca pelo model(modelo do carro)

    return render(
        
        request,
         'cars.html', {'cars': cars})

# As duas formas funcional porem ClassbaseView é o mais recomandado 
class CarsView(View):

    def get(self, request):
      cars = Car.objects.all()
      search = request.GET.get('search')

      if search:
        cars = Car.objects.filter(model__icontains=search) # Buaca pelo model(modelo do carro)

      return render(
          
          request,
          'cars.html', {'cars': cars})


 # A funçao é a mesma que as decima porem quando uso LISTVIEW eu uso menos linhas e o class ja faz tudo sozinha

class CarsListView(ListView):
   model = Car
   template_name = 'cars.html'
   context_object_name = 'cars'

   #Se quiser fazer uma busca no BD
   def get_queryset(self):
    cars = super().get_queryset().order_by('model')
    search = self.request.GET.get('search')
    if search:
      cars = cars.filter(model__icontains=search)
    return cars  
                

def new_car_view(request):

  if request.method =='POST':
    #Recebendo dados do formulario
    new_car_form = CarModelForm(request.POST, request.FILES)
    #verificados se os dados são validos
    if new_car_form.is_valid():
      new_car_form.save() #chamando def save q esta CarForm
      return redirect('cars_list') #direcionado para pg car_list
  else:
    new_car_form = CarModelForm() #GET em CarForm
  return render(request, 'new_car.html', { 'new_car_form' : new_car_form })


# As duas formas funcional porem ClassbaseView é o mais recomandado 
class NewCarView(View):

  def get(self,request):
    new_car_form = CarModelForm() #GET em CarForm
    return render(request, 'new_car.html', { 'new_car_form' : new_car_form })

  def post(self,request):    
      #Recebendo dados do formulario
      new_car_form = CarModelForm(request.POST, request.FILES)
      #verificados se os dados são validos
      if new_car_form.is_valid():
        new_car_form.save() #chamando def save q esta CarForm
        return redirect('cars_list') #direcionado para pg car_list
      return render(request, 'new_car.html', { 'new_car_form' : new_car_form })

#method decorator teste se acessão esta ativa(login) se não manda para tela de login
@method_decorator(login_required(login_url='login'), name='dispatch')     
# Class CreateView mais curto e obtivo porem no arquvi html tem ficar  dessa forma  {{ form.as_table }}
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars'         

 
# Criar uma pagina com detalhes do Carro
class CarDetailView(DetailView):
  model = Car
  template_name = 'car_detail.html'
  
#method decorator teste se acessão esta ativa(login) se não manda para tela de login
@method_decorator(login_required(login_url='login'), name='dispatch') 
class CarUpdateView(UpdateView):
  model = Car
  form_class = CarModelForm
  template_name = 'car_update.html'
  def get_success_url(self):
    #reverse_lazy pega nome(car_detail) e passa o argumneto esperado na url no caso pk
    return reverse_lazy('car_detail', kwargs={'pk': self.object.pk}) 

#method decorator teste se acessão esta ativa(login) se não manda para tela de login
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
  model = Car
  template_name = 'car_delete.html'
  success_url = '/cars/'  
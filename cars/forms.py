from django import forms
from cars.models import Brand,Car

class Carform(forms.Form):
    model = forms.CharField(max_length=200)
    brand = forms.ModelChoiceField(Brand.objects.all())
    factory_year = forms.IntegerField()
    model_year = forms.IntegerField()
    value = forms.FloatField()
    photo = forms.ImageField()

    def save(self):
        # Instancia Car com os dados do Form
        car = Car(
            model = self.cleaned_data['model'],
            brand = self.cleaned_data['brand'],
            factory_year = self.cleaned_data['factory_year'],
            model_year = self.cleaned_data['model_year'],
            value =self.cleaned_data['value'],
            photo = self.cleaned_data['photo'],
        )
        car.save()  #salva no Banco de Dados
        return car

   # As duas class faz a mesma funçao a diferença que com model a hora que alterar no DB o furmulario altera automaticamante

class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
    # metodo de validação deve sempre começar "clean_" +nome do campo do formulario
    def clean_value(self):
        value = self.cleaned_data.get('value')  #Pega os dados formulario campo clean_value
        #regra 
        if value < 5000:
            #add_erro(primeiro campo do formulario e seguinda o aviso erro)
            self.add_error('value','Só é aceito Valores acima de R$ 5 Mil')
        return value

    
from django import forms
from .models import Viatura, Checklist


class ViaturaForm(forms.ModelForm):

    class Meta:
        model = Viatura
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ChecklistForm(forms.ModelForm):

    # Campo troca de óleo como Radio Button
    troca_oleo = forms.ChoiceField(
        choices=[("sim", "Sim"), ("nao", "Não")],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Checklist
        exclude = ["usuario"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            # Não aplicar form-control no radio button
            if name != "troca_oleo":
                field.widget.attrs.update({'class': 'form-control'})
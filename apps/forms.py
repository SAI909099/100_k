from django.forms import ModelForm

from apps.models import Stream


class StreamForm(ModelForm):
    class Meta:
        model = Stream
        fields = 'name', 'discount', 'product', 'owner'

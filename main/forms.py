from django import forms
from django.forms.models import modelformset_factory
from django.forms.models import BaseModelFormSet
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField, AutoCompleteField

from .models import RFK

class KategooriaForm(forms.Form):
    kategooria = AutoCompleteSelectMultipleField(
        'kategooriad',
        required=False,
        help_text='',
        plugin_options={'autoFocus': True, 'minLength': 2},
        label=''
    )

    class Media:
        # js = ["/static/admin/js/jquery.init.js"]
        pass

M22RAJAD = [(str(m22raja), str(m22raja)) for m22raja in [''] + [*range(0, 10)]]

class ArticleForm(forms.Form):
    kategooria = AutoCompleteField(
        'kategooriad',
        required=False,
        help_text='',
        plugin_options={'autoFocus': True, 'minLength': 2}
    )
    m22raja2 = forms.ChoiceField(
        widget=forms.Select,
        choices=M22RAJAD,
        label=" "
    )
    m22raja3 = forms.ChoiceField(
        widget=forms.Select,
        choices=M22RAJAD,
        label=' '
    )

from django.forms import BaseFormSet, formset_factory


class BaseArticleFormSet(BaseFormSet):
    pass

ArticleFormSet = formset_factory(
    ArticleForm,
    formset=BaseArticleFormSet,
    # can_order=True,
    # can_delete=True,
    extra=1
)
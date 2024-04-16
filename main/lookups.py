from django.db.models.functions import Concat
from django.db.models import F, Value, CharField
from django.db.models.functions import Length

from ajax_select import register, LookupChannel

from .models import RFK
from .views import get_icf_code_verbose

class Item:

    def __init__(self, pk, value, match, repr):
        self.pk = pk
        self.value = value
        self.match = match
        self.repr = repr

@register('kategooriad')
class KategooriaLookup(LookupChannel):

    model = RFK

    def check_auth(self, request):
        return True

    def get_query(self, q, request):
        if len(q) > 3 and (('.' == q[-1]) or (q[0].lower() == 'e' and '+' == q[-1])):
            queryset = [
                Item(
                    pk=RFK.objects.filter(code__exact=q[:-1])[0].pk,
                    value=f'{q}{m22raja}',
                    match=get_icf_code_verbose(request=None, code=f'{q}{m22raja}', flat=True),
                    repr=get_icf_code_verbose(request=None, code=f'{q}{m22raja}', flat=True),
                ) for
                m22raja in
                [0, 1, 2, 3, 4, 8, 9]
            ]
        elif len(q) > 3 and '.' == q[-2] and (q[0].lower() in ['b']):
            kategooria, m22raja = q.split('.')
            queryset = [
                Item(
                    pk=RFK.objects.filter(code__exact=kategooria)[0].pk,
                    value=f'{q}',
                    match=get_icf_code_verbose(request=None, code=f'{q}', flat=True),
                    repr=get_icf_code_verbose(request=None, code=f'{q}', flat=True),
                )
            ]
        elif len(q) > 3 and '.' == q[-2] and (q[0].lower() in ['d', 's']):
            m22rajad = ['', 0, 1, 2, 3, 4, 8, 9]
            if q[0].lower() == 's':
                m22rajad = [''] + [*range(0, 10)]
            queryset = [
                Item(
                    pk=RFK.objects.filter(code__exact=q[:-2])[0].pk,
                    value=f'{q}{m22raja}',
                    match=get_icf_code_verbose(request=None, code=f'{q}{m22raja}', flat=True),
                    repr=get_icf_code_verbose(request=None, code=f'{q}{m22raja}', flat=True),
                ) for
                m22raja in
                m22rajad
            ]
        elif len(q) > 3 and '.' == q[-3] and (q[0].lower() in ['s']):
            m22rajad = [''] + [*range(0, 10)]
            queryset = [
                Item(
                    pk=RFK.objects.filter(code__exact=q[:-3])[0].pk,
                    value=f'{q}{m22raja}',
                    match=get_icf_code_verbose(request=None, code=f'{q}{m22raja}', flat=True),
                    repr=get_icf_code_verbose(request=None, code=f'{q}{m22raja}', flat=True),
                ) for
                m22raja in
                m22rajad
            ]
        else:
            splits = q.split(' ')
            queryset = self.model.objects.annotate(
                length=Length('code'),
                nimi=Concat(
                    F('code'),
                    Value(' '),
                    F('Translated_title'),
                    output_field=CharField()
                )
            )
            queryset = queryset.filter(length__gt=3, length__lt=7)
            for split in splits:
                queryset = queryset.filter(nimi__icontains=split)
        return queryset

    def format_match(self, item):
        """ (HTML) formatted item for display in the dropdown """
        if isinstance(item, RFK):
            answer = f'{item.code} {item.Translated_title}'
        else:
            answer = item.match
        return answer

    def format_item_display(self, item):
        """ (HTML) formatted item for displaying item in the selected deck area """
        if isinstance(item, RFK):
            answer = f'{item.code}'
        else:
            answer = get_icf_code_verbose(request=None, code=item.value, flat=True)
        return answer

    def get_result(self, item):
        if isinstance(item, RFK):
            answer = f'{item.code}'
        else:
            # answer = item.split(' ')[0]
            answer = item.value
        return answer

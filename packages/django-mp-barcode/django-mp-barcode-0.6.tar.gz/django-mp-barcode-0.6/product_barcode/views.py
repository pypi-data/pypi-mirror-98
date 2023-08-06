
from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required

from product_barcode.models import BarCode


@staff_member_required
def get_code(request, code):

    try:
        img = BarCode.get_image(code)
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseBadRequest(str(e))

    response = HttpResponse(content_type='image/png')

    img.save(response, 'png')

    return response


@staff_member_required
def print_codes(request):
    codes_str = request.GET.get('codes', '')
    codes = codes_str.split(',') if codes_str else ''
    return render(request, 'barcode/print.html', {'codes': codes})

from django.db.models import Q
from django.http import HttpResponse
from .views import staff_member_required
from ..utils import render_to_pdf, image64
from datetime import date
from .models import SalePoint


@staff_member_required
def pdf( request ):

	if request.is_ajax():
		q = request.GET.get( 'q' )

		type = None
		if q is not None:
			points = SalePoint.objects.filter(
				Q(name__icontains=q)).order_by('id')

		else:
			points = SalePoint.objects.all()
		img = image64()
		data = {
			'today': date.today(),
			'points': points,
			'puller': request.user,
			'image': img,
			'type':type
		}
		pdf = render_to_pdf('dashboard/salepoints/pdf/pdf.html', data)
		return HttpResponse(pdf, content_type='application/pdf')

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from saleor.dashboard.views import staff_member_required
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import SalePoint


@staff_member_required
def search_point(request):
	if request.is_ajax():
		page = request.GET.get('page', 1)
		list_sz = request.GET.get('size')
		p2_sz = request.GET.get('psize')
		q = request.GET.get('q')

		if list_sz == 0 or list_sz is None:
			sz = 10
		else:
			sz = list_sz

		if q is not None:
			points = SalePoint.objects.filter(
				Q(name__icontains=q)).order_by('id')

			if list_sz:
				paginator = Paginator(points, int(list_sz))
				points = paginator.page(page)
				return TemplateResponse(request, 'dashboard/salepoints/search.html',
										{'points': points, 'pn': paginator.num_pages, 'sz': list_sz, 'gid': 0,
										 'q': q})

			if p2_sz:
				paginator = Paginator(points, int(p2_sz))
				points = paginator.page(page)
				return TemplateResponse(request, 'dashboard/salepoints/paginate.html',
										{'points': points})

			paginator = Paginator(points, 10)
			try:
				points = paginator.page(page)
			except PageNotAnInteger:
				points = paginator.page(1)
			except InvalidPage:
				points = paginator.page(1)
			except EmptyPage:
				points = paginator.page(paginator.num_pages)
			return TemplateResponse(request, 'dashboard/salepoints/search.html',
									{'points': points, 'pn': paginator.num_pages, 'sz': sz, 'q': q})


@staff_member_required
def paginate_point(request):
	page = int(request.GET.get('page', 1))
	list_sz = request.GET.get('size')
	p2_sz = request.GET.get('psize')

	try:
		points = SalePoint.objects.all().order_by('-id')
		if list_sz:
			paginator = Paginator(points, int(list_sz))
			points = paginator.page(page)
			data = {
				'points': points,
				'pn': paginator.num_pages,
				'sz': list_sz,
				'gid': 0
			}
			return TemplateResponse(request, 'dashboard/salepoints/p2.html', data)
		else:
			paginator = Paginator(points, 10)
		if p2_sz:
			paginator = Paginator(points, int(p2_sz))
			points = paginator.page(page)
			data = {
				"points": points
			}
			return TemplateResponse(request, 'dashboard/salepoints/paginate.html', data)

		try:
			points = paginator.page(page)
		except PageNotAnInteger:
			points = paginator.page(1)
		except InvalidPage:
			points = paginator.page(1)
		except EmptyPage:
			points = paginator.page(paginator.num_pages)
		return TemplateResponse(request, 'dashboard/salepoints/paginate.html', {"points": points})
	except Exception, e:
		return HttpResponse(e)
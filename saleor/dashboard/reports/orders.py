from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
import datetime
from django.utils.dateformat import DateFormat
import logging
from ..views import staff_member_required
from ...sale.models import Sales, SoldItem
from ...decorators import permission_decorator, user_trail

debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


@staff_member_required
@permission_decorator('reports.view_sale_reports')
def sales_list(request):
	try:
		try:
			last_sale = Sales.objects.latest('id')
			last_date_of_sales = DateFormat(last_sale.created).format('Y-m-d')
		except:
			last_date_of_sales = DateFormat(datetime.datetime.today()).format('Y-m-d')

		all_sales = Sales.objects.filter(created__contains=last_date_of_sales)
		total_sales_amount = all_sales.aggregate(Sum('total_net'))
		total_tax_amount = all_sales.aggregate(Sum('total_tax'))
		total_sales = []
		for sale in all_sales:
			quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Sum('quantity'))
			setattr(sale, 'quantity', quantity['c'])
			total_sales.append(sale)

		page = request.GET.get('page', 1)
		paginator = Paginator(total_sales, 10)
		try:
			total_sales = paginator.page(page)
		except PageNotAnInteger:
			total_sales = paginator.page(1)
		except InvalidPage:
			total_sales = paginator.page(1)
		except EmptyPage:
			total_sales = paginator.page(paginator.num_pages)
		user_trail(request.user.name, 'accessed sales reports', 'view')
		info_logger.info('User: ' + str(request.user.name) + ' accessed the view sales report page')
		return TemplateResponse(request, 'dashboard/reports/orders/sales_list.html',
								{'pn': paginator.num_pages, 'sales': total_sales,
								 "total_sales_amount": total_sales_amount, "total_tax_amount": total_tax_amount,
								 "date": last_date_of_sales})
	except ObjectDoesNotExist as e:
		error_logger.error(e)


@staff_member_required
@permission_decorator('reports.view_sale_reports')
def sales_detail(request, pk=None):
	try:
		sale = Sales.objects.get(pk=pk)
		items = SoldItem.objects.filter(sales=sale)

		# try:
		# 	baritems = SoldItem.objects.filter(sales=sale, salepoint__name='bar')
		# 	baritems_total = baritems.aggregate(Sum('total_cost'))['total_cost__sum']
		# 	baritems_tax = baritems.aggregate(Sum('tax'))['tax__sum']
		# 	baritems_discount = baritems.aggregate(Sum('discount'))['discount__sum']
		# 	if not baritems.exists():
		# 		raise Exception
		# except Exception as e:
		# 	baritems = None
		# 	baritems_total = 0
		# 	baritems_tax = 0
		# 	baritems_discount = 0
		#
		# try:
		# 	restitems = SoldItem.objects.filter(sales=sale, salepoint__name='restaurant')
		# 	restitems_total = restitems.aggregate(Sum('total_cost'))['total_cost__sum']
		# 	restitems_tax = restitems.aggregate(Sum('tax'))['tax__sum']
		# 	restitems_discount = restitems.aggregate(Sum('discount'))['discount__sum']
		#
		# 	if not restitems.exists():
		# 		raise Exception
		# except Exception as e:
		# 	restitems = None
		# 	restitems_total = 0
		# 	restitems_tax = 0
		# 	restitems_discount = 0


		data = {
			'items': items,
			'sale': sale,

			# 'baritems':baritems,
			# 'baritems_total':baritems_total,
			# 'baritems_tax':baritems_tax,
			# 'baritems_discount':baritems_discount,
			#
			# 'restitems':restitems,
			# 'restitems_total':restitems_total,
			# 'restitems_tax':restitems_tax,
			# 'restitems_discount':restitems_discount
		}
		return TemplateResponse(request, 'dashboard/reports/orders/details.html', data)
	except ObjectDoesNotExist as e:
		error_logger.error(e)


@staff_member_required
def sales_paginate(request):
	page = int(request.GET.get('page'))
	list_sz = request.GET.get('size')
	p2_sz = request.GET.get('psize')
	select_sz = request.GET.get('select_size')
	date = request.GET.get('gid')
	sales = Sales.objects.all().order_by('-id')
	today_formart = DateFormat(datetime.date.today())
	today = today_formart.format('Y-m-d')
	ts = Sales.objects.filter(created__icontains=today)
	tsum = ts.aggregate(Sum('total_net'))
	total_sales = Sales.objects.aggregate(Sum('total_net'))
	total_tax = Sales.objects.aggregate(Sum('total_tax'))

	if date:
		try:
			all_salesd = Sales.objects.filter(created__icontains=date).order_by('-id')
			that_date_sum = Sales.objects.filter(created__contains=date).aggregate(Sum('total_net'))
			sales = []
			for sale in all_salesd:
				quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
				setattr(sale, 'quantity', quantity['c'])
				sales.append(sale)

			if p2_sz and date:
				paginator = Paginator(sales, int(p2_sz))
				sales = paginator.page(page)
				return TemplateResponse(request, 'dashboard/reports/orders/paginate.html', {'sales': sales, 'gid': date})

			paginator = Paginator(sales, 10)
			sales = paginator.page(page)
			return TemplateResponse(request, 'dashboard/reports/orders/p2.html',
									{'sales': sales, 'pn': paginator.num_pages, 'sz': 10, 'gid': date,
									 'total_sales': total_sales, 'total_tax': total_tax, 'tsum': tsum,
									 'that_date_sum': that_date_sum, 'date': date, 'today': today})

		except ObjectDoesNotExist as e:
			return TemplateResponse(request, 'dashboard/reports/orders/p2.html', {'date': date})

	else:
		try:
			last_sale = Sales.objects.latest('id')
			last_date_of_sales = DateFormat(last_sale.created).format('Y-m-d')
			all_sales = Sales.objects.filter(created__contains=last_date_of_sales)
			total_sales_amount = all_sales.aggregate(Sum('total_net'))
			total_tax_amount = all_sales.aggregate(Sum('total_tax'))
			sales = []
			for sale in all_sales:
				quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
				setattr(sale, 'quantity', quantity['c'])
				sales.append(sale)

			if list_sz:
				paginator = Paginator(sales, int(list_sz))
				sales = paginator.page(page)
				return TemplateResponse(request, 'dashboard/reports/orders/p2.html',
										{'sales': sales, 'pn': paginator.num_pages, 'sz': list_sz, 'gid': 0,
										 'total_sales': total_sales, 'total_tax': total_tax, 'tsum': tsum})
			else:
				paginator = Paginator(sales, 10)
			if p2_sz:
				paginator = Paginator(sales, int(p2_sz))
				sales = paginator.page(page)
				return TemplateResponse(request, 'dashboard/reports/orders/paginate.html', {'sales': sales})

			try:
				sales = paginator.page(page)
			except PageNotAnInteger:
				sales = paginator.page(1)
			except InvalidPage:
				sales = paginator.page(1)
			except EmptyPage:
				sales = paginator.page(1)
			return TemplateResponse(request, 'dashboard/reports/orders/paginate.html', {'sales': sales})
		except ObjectDoesNotExist as e:
			return TemplateResponse(request, 'dashboard/reports/orders/p2.html', {'date': date})


@staff_member_required
def sales_search(request):
	if request.is_ajax():
		page = int(request.GET.get('page', 1))
		list_sz = request.GET.get('size')
		p2_sz = request.GET.get('psize')
		q = request.GET.get('q')
		if list_sz is None:
			sz = 10
		else:
			sz = list_sz

		if q is not None:
			all_sales = Sales.objects.filter(
				Q(invoice_number__icontains=q) |
				Q(terminal__terminal_name__icontains=q) |
				Q(created__icontains=q) |
				Q(customer__name__icontains=q) | Q(customer__mobile__icontains=q) |
				Q(solditems__product_name__icontains=q) |
				Q(user__email__icontains=q) |
				Q(user__name__icontains=q)).order_by('id').distinct()
			sales = []

			if request.GET.get('gid'):
				csales = all_sales.filter(created__icontains=request.GET.get('gid'))
				for sale in csales:
					quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
					setattr(sale, 'quantity', quantity['c'])
					sales.append(sale)

				if p2_sz:
					paginator = Paginator(sales, int(p2_sz))
					sales = paginator.page(page)
					return TemplateResponse(request, 'dashboard/reports/orders/paginate.html', {'sales': sales})

				if list_sz:
					paginator = Paginator(sales, int(list_sz))
					sales = paginator.page(page)
					return TemplateResponse(request, 'dashboard/reports/orders/search.html',
											{'sales': sales, 'pn': paginator.num_pages, 'sz': list_sz,
											 'gid': request.GET.get('gid'), 'q': q})

				paginator = Paginator(sales, 10)
				sales = paginator.page(page)
				return TemplateResponse(request, 'dashboard/reports/orders/search.html',
										{'sales': sales, 'pn': paginator.num_pages, 'sz': sz,
										 'gid': request.GET.get('gid')})

			else:
				for sale in all_sales:
					quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
					setattr(sale, 'quantity', quantity['c'])
					sales.append(sale)

				if list_sz:
					print ('lst')
					paginator = Paginator(sales, int(list_sz))
					sales = paginator.page(page)
					return TemplateResponse(request, 'dashboard/reports/orders/search.html',
											{'sales': sales, 'pn': paginator.num_pages, 'sz': list_sz, 'gid': 0,
											 'q': q})

				if p2_sz:
					print ('pst')
					paginator = Paginator(sales, int(p2_sz))
					sales = paginator.page(page)
					return TemplateResponse(request, 'dashboard/reports/orders/paginate.html', {'sales': sales})

				paginator = Paginator(sales, 10)
				try:
					sales = paginator.page(page)
				except PageNotAnInteger:
					sales = paginator.page(1)
				except InvalidPage:
					sales = paginator.page(1)
				except EmptyPage:
					sales = paginator.page(paginator.num_pages)
				if p2_sz:
					sales = paginator.page(page)
					return TemplateResponse(request, 'dashboard/reports/orders/paginate.html', {'sales': sales})

				return TemplateResponse(request, 'dashboard/reports/orders/search.html',
										{'sales': sales, 'pn': paginator.num_pages, 'sz': sz, 'q': q})


@staff_member_required
def sales_list_pdf( request ):

	if request.is_ajax():
		q = request.GET.get( 'q' )
		gid = request.GET.get('gid')

		if gid:
			gid = gid
		else:
			gid = None

		sales = []
		if q is not None:
			all_sales = Sales.objects.filter(
				Q(invoice_number__icontains=q) |
				Q(terminal__terminal_name__icontains=q) |
				Q(created__icontains=q) |
				Q(customer__name__icontains=q) | Q(customer__mobile__icontains=q) |
				Q(solditems__product_name__icontains=q) |
				Q(user__email__icontains=q) |
				Q(user__name__icontains=q)).order_by('id').distinct()

			if gid:
				csales = all_sales.filter(created__icontains=gid)
				for sale in csales:
					quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
					setattr(sale, 'quantity', quantity['c'])
					sales.append(sale)
			else:
				for sale in all_sales:
					quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
					setattr(sale, 'quantity', quantity['c'])
					sales.append(sale)

		elif gid:
			csales = Sales.objects.filter(created__icontains=gid)
			for sale in csales:
				quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
				setattr(sale, 'quantity', quantity['c'])
				sales.append(sale)
		else:
			try:
				last_sale = Sales.objects.latest('id')
				gid = DateFormat(last_sale.created).format('Y-m-d')
			except:
				gid = DateFormat(datetime.datetime.today()).format('Y-m-d')

			csales = Sales.objects.filter(created__icontains=gid)
			for sale in csales:
				quantity = SoldItem.objects.filter(sales=sale).aggregate(c=Count('sku'))
				setattr(sale, 'quantity', quantity['c'])
				sales.append(sale)

		img = default_logo
		data = {
			'today': date.today(),
			'sales': sales,
			'puller': request.user,
			'image': img,
			'gid':gid
		}
		pdf = render_to_pdf('dashboard/reports/sales/pdf/saleslist_pdf.html', data)
		return HttpResponse(pdf, content_type='application/pdf')
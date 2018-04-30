from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Min, Sum, Avg, Max
from django.core import serializers
from django.template.defaultfilters import date
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import datetime
from datetime import date, timedelta
from django.utils.dateformat import DateFormat
import logging
import random
import csv
from django.utils.encoding import smart_str
from decimal import Decimal
from calendar import monthrange
import calendar
from django_xhtml2pdf.utils import generate_pdf

import re
import base64

from ..core.utils import get_paginator_items
from ..dashboard.views import staff_member_required
from ..userprofile.models import User, Staff
from ..supplier.models import Supplier
from ..customer.models import Customer
from ..sale.models import Sales, SoldItem, Terminal
from ..product.models import Product, ProductVariant, Category
from ..decorators import permission_decorator, user_trail
from ..utils import render_to_pdf, convert_html_to_pdf
from ..site.models import UserRole, Department, BankBranch, Bank
from ..expensetypes.models import ExpenseTypes as ExpenseType

debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')



@staff_member_required
def add(request):
	expense_type = request.POST.get('expense_type')
	option = request.POST.get('option')
	new_expense = ExpenseType(name=expense_type)
	if option:
		try:
			new_expense.save()
			expense_types = ExpenseType.objects.all()
			data = {"expense_types": expense_types}
			return TemplateResponse(request, 'dashboard/sites/hr/select_role.html', data)
		except IntegrityError as e:
			error_logger.error(e)
			return HttpResponse('error')
		except ValidationError as e:
			error_logger.error(e)
			return HttpResponse('error')
	else:
		try:
			new_expense_type.save()
			expense_types = ExpenseType.objects.all()
			data = {"expense_types": expense_types}
			return TemplateResponse(request, 'dashboard/sites/hr/department.html', data)
		except IntegrityError as e:
			error_logger.error(e)
			return HttpResponse('error')
		except ValidationError as e:
			error_logger.error(e)
			return HttpResponse('error')

def delete(request, pk):
	expense_type = get_object_or_404(ExpenseType, pk=pk)
	if request.method == 'POST':
		expense_type.delete()
		user_trail(request.user.name, 'deleted expense_type: '+ str(expense_type.name),'delete')
		return HttpResponse('success')

def edit(request, pk):
	expense_type = get_object_or_404(ExpenseType, pk=pk)
	if request.method == 'POST':
		new_expense_type = request.POST.get('department')
		expense_type.name = new_expense_type
		expense_type.save()
		user_trail(request.user.name, 'updated expense_type from: '+ str(expense_type.name) + ' to: '+str(new_expense_type),'update')
		return HttpResponse('success')
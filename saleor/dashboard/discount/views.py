from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
import csv
from django.http import HttpResponse

from ...discount.models import Sale, Voucher
from . import forms


@staff_member_required
def sale_list(request):
    sales = Sale.objects.prefetch_related('products')
    ctx = {'sales': sales}
    return TemplateResponse(request, 'dashboard/discount/sale_list.html', ctx)


@staff_member_required
def sale_edit(request, pk=None):
    if pk:
        instance = get_object_or_404(Sale, pk=pk)
    else:
        instance = Sale()
    form = forms.SaleForm(
        request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        msg = _('Updated sale') if pk else _('Added sale')
        messages.success(request, msg)
        return redirect('dashboard:sale-update', pk=instance.pk)
    ctx = {'sale': instance, 'form': form}
    return TemplateResponse(request, 'dashboard/discount/sale_form.html', ctx)


@staff_member_required
def sale_delete(request, pk):
    instance = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        instance.delete()
        messages.success(
            request, _('Deleted sale %s') % (instance.name,))
        return redirect('dashboard:sale-list')
    ctx = {'sale': instance}
    return TemplateResponse(
        request, 'dashboard/discount/sale_modal_confirm_delete.html', ctx)


@staff_member_required
def voucher_list(request):
    vouchers = Voucher.objects.select_related('product', 'category')
    ctx = {'vouchers': vouchers}
    return TemplateResponse(
        request, 'dashboard/discount/voucher_list.html', ctx)


@staff_member_required
def voucher_edit(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Voucher, pk=pk)
    else:
        instance = Voucher()
    voucher_form, type_base_forms = _create_forms(request, instance)
    if voucher_form.is_valid():
        group = voucher_form.cleaned_data['group']
        voucher_type = voucher_form.cleaned_data['type']
        form_type = type_base_forms.get(voucher_type)
        if group:
            count = voucher_form.cleaned_data['count']
            group_id = forms.VoucherForm.generate_code()
            for index in range(0, count):
                instance.id = None
                instance.code = forms.VoucherForm.generate_code()
                instance.group_id = group_id
                voucher_form, type_base_forms = _create_forms(request, instance)
                form_type = type_base_forms.get(voucher_type)
                _save_form(voucher_form, form_type)

            if form_type is None or form_type.is_valid():
                msg = _('Created group of vouchers')
                messages.success(request, msg)
                return redirect('dashboard:voucher-list')

        else:
            instance = _save_form(voucher_form, form_type)

            if form_type is None or form_type.is_valid():
                msg = _('Updated voucher') if pk else _('Added voucher')
                messages.success(request, msg)
                return redirect('dashboard:voucher-update', pk=instance.pk)
    ctx = {
        'voucher': instance, 'default_currency': settings.DEFAULT_CURRENCY,
        'form': voucher_form, 'type_base_forms': type_base_forms}
    return TemplateResponse(
        request, 'dashboard/discount/voucher_form.html', ctx)


def _save_form(voucher_form, form_type):
    if form_type is None:
        instance = voucher_form.save()
    elif form_type.is_valid():
        instance = form_type.save()
    return instance


def _create_forms(request, instance):
    voucher_form = forms.VoucherForm(request.POST or None, instance=instance)
    type_base_forms = {
        Voucher.SHIPPING_TYPE: forms.ShippingVoucherForm(
            request.POST or None, instance=instance,
            prefix=Voucher.SHIPPING_TYPE),
        Voucher.VALUE_TYPE: forms.ValueVoucherForm(
            request.POST or None, instance=instance,
            prefix=Voucher.VALUE_TYPE),
        Voucher.PRODUCT_TYPE: forms.ProductVoucherForm(
            request.POST or None, instance=instance,
            prefix=Voucher.PRODUCT_TYPE),
        Voucher.CATEGORY_TYPE: forms.CategoryVoucherForm(
            request.POST or None, instance=instance,
            prefix=Voucher.CATEGORY_TYPE)}
    return voucher_form, type_base_forms


@staff_member_required
def voucher_delete(request, pk):
    instance = get_object_or_404(Voucher, pk=pk)
    if request.method == 'POST':
        instance.delete()
        messages.success(
            request, _('Deleted voucher %s') % (instance,))
        return redirect('dashboard:voucher-list')
    ctx = {'voucher': instance}
    return TemplateResponse(
        request, 'dashboard/discount/voucher_modal_confirm_delete.html', ctx)


@staff_member_required
def voucher_delete_group(request, pk):
    instance = get_object_or_404(Voucher, pk=pk)
    if request.method == 'POST':
        Voucher.objects.filter(group_id=instance.group_id).delete()
        messages.success(
            request, _('Deleted voucher group %s') % (instance,))
        return redirect('dashboard:voucher-list')
    ctx = {'voucher': instance}
    return TemplateResponse(
        request, 'dashboard/discount/voucher_modal_confirm_delete_group.html', ctx)


@staff_member_required
def voucher_export_group(request, pk):
    instance = get_object_or_404(Voucher, pk=pk)
    if request.method == 'POST':
        vouchers = Voucher.objects.filter(group_id=instance.group_id).all()
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="group-{0}.csv"'.format(vouchers[0].group_id)

        writer = csv.writer(response)
        for voucher in vouchers:
            writer.writerow([voucher.code])
        messages.success(
            request, _('Deleted voucher %s') % (instance,))
        # return redirect('dashboard:voucher-list')
        return response
    ctx = {'voucher': instance}
    return TemplateResponse(
        request, 'dashboard/discount/voucher_modal_confirm_export_group.html', ctx)

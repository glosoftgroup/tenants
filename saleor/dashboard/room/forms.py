from __future__ import unicode_literals

from django import forms
from django.db import transaction
from django.db.models import Count
from django.forms.models import ModelChoiceIterator, inlineformset_factory
from django.utils.encoding import smart_text
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy

from saleor.room.models import RoomImage, RoomVariant, Room


class RoomImageForm(forms.ModelForm):
    variants = forms.ModelMultipleChoiceField(
        queryset=RoomVariant.objects.none(),
        widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = RoomImage
        exclude = ('room', 'order')

    def __init__(self, *args, **kwargs):
        super(RoomImageForm, self).__init__(*args, **kwargs)
        show_variants = self.instance.room.room_class.has_variants
        if self.instance.room and show_variants:
            variants = self.fields['room_variants']
            variants.queryset = self.instance.room.variants.all()
            variants.initial = self.instance.variant_images.values_list(
                'variant', flat=True)
        if self.instance.image:
            field = self.fields['image']
            field.widget.attrs['class'] = 'file-styled'
        field = self.fields['alt']
        field.widget.attrs['class'] = 'form-control'

        field = self.fields['variants']
        field.widget.attrs['class'] = 'styled'


    @transaction.atomic
    def save_variant_images(self, instance):
        variant_images = []
        # Clean up old mapping
        instance.variant_images.all().delete()
        for variant in self.cleaned_data['variants']:
            variant_images.append(
                VariantImage(variant=variant, image=instance))
        VariantImage.objects.bulk_create(variant_images)

    def save(self, commit=True):
        instance = super(ProductImageForm, self).save(commit=commit)
        self.save_variant_images(instance)
        return instance


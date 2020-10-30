from io import BytesIO
from PIL import Image

from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        product_image = self.cleaned_data.get('image')
        if product_image and 'image' in self.changed_data:
            image_file = BytesIO(product_image.read())
            image = Image.open(image_file)
            w, h = image.size

            image = image.resize((w, w // 4 * 3), Image.ANTIALIAS)

            image_file = BytesIO()
            image.save(image_file, "JPEG", quality=90)

            product_image.file = image_file
            self.cleaned_data['image'] = product_image

        return self.cleaned_data

from django import forms
from .models import Product, SubCategory, ProductType, Category, ProductImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductForm(forms.ModelForm):

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if stock is not None:
            if stock < 1:
                raise forms.ValidationError("Stock cannot be 0. Please add at least 1 item.")
            if stock > 50:
                raise forms.ValidationError("Stock cannot exceed 50 units per listing.")

        return stock

    class Meta:
        model = Product
        # exclude = ['seller', 'category', 'subcategory', 'product_type','created_at']
        fields=['name','description','price','stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4 }),

            'price': forms.NumberInput(attrs={'class': 'form-control' }),

            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
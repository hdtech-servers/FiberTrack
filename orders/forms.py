from django import forms
from .models import OrderItem, Order
from inventory.models import Product

class OrderForm(forms.ModelForm):
    # Payment option field to allow choosing between "Pay Now" or "Pay on Delivery"
    PAYMENT_OPTIONS = [
        ('pay_now', 'Pay Now'),
        ('pay_on_delivery', 'Pay on Delivery'),
    ]
    payment_option = forms.ChoiceField(
        choices=PAYMENT_OPTIONS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Payment Option"
    )

    # Paid amount field for "Pay Now" option
    paid_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Amount Paid"
    )

    class Meta:
        model = Order
        fields = ['supplier', 'payment_option', 'paid_amount']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['paid_amount'].widget.attrs.update({'placeholder': 'Enter paid amount if Pay Now is selected'})

    def clean(self):
        cleaned_data = super().clean()
        payment_option = cleaned_data.get('payment_option')
        paid_amount = cleaned_data.get('paid_amount')

        # Ensure paid amount is provided if "Pay Now" is selected
        if payment_option == 'pay_now' and (paid_amount is None or paid_amount <= 0):
            self.add_error('paid_amount', 'Please enter a valid paid amount for Pay Now option.')

        return cleaned_data


class OrderItemForm(forms.ModelForm):
    # Fields for selecting product and setting quantity and price
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="-- Select a Product --"
    )
    quantity_ordered = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Quantity Ordered"
    )
    buying_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Buying Price"
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity_ordered', 'buying_price']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Set initial buying price based on the product
            self.fields['buying_price'].initial = self.instance.product.buying_price
        else:
            self.fields['buying_price'].initial = None

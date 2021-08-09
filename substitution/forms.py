from django import forms

# RATING_CHOICES=[
#     (0,'A fuir'),
#     (0,'A éviter'),
#     (0,'Neutre'),
#     (0,'J\'apprécie'),
#     (0,'J\'adore'),
# ]

RATING_CHOICES=[
    tuple([x,x]) for x in range(0,5)
]

class RatingForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    rating=forms.IntegerField(widget=forms.Select(choices=RATING_CHOICES))


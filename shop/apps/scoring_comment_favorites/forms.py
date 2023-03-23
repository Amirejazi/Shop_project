from django import forms


class CommentForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_text = forms.CharField(
                            label="",
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'متن نظر', 'rows': '4'}),
                            error_messages={'required': "این فیلد نمیتواند خالی باشد!"})

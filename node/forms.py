from django import forms


class NodeForm(forms.Form):
    title = forms.CharField(max_length=140)
    body = forms.CharField(widget=forms.Textarea)
    author = forms.CharField(max_length=140)
    revision_log = forms.CharField(max_length=250)
    is_front_page = forms.BooleanField(required=False)
    is_sticky = forms.BooleanField(required=False)
    is_published = forms.BooleanField(required=False)
    can_comment = forms.BooleanField(required=False)
    # tags = forms.CharField(max_length=500)
    node_type = forms.CharField(max_length=100)
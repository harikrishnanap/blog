from django import forms
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkbox'}),
        label="Select Categories",
        required=False  # Optional but useful
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SearchForm(forms.Form):
    # query = forms.CharField(label='Search', max_length=100)
    query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts...',
            'class': 'form-control'
        })
    )


    # dropdown checklist
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.SelectMultiple(attrs={
    #         'class': 'form-control',
    #         'size': '5',  # shows 5 items at once
    #         'style': 'min-height: 120px;'
    #     }),
    #     label="Select Categories",
    #     help_text = "Hold Ctrl (Windows) or Cmd (Mac) to select multiple"
    # )
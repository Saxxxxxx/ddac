from django import forms
from .models import EducationArticleHeader,EducationArticleBody

class EducationArticleForm(forms.ModelForm):
    article_body_content = forms.CharField(widget=forms.Textarea)  # Add field for article body content

    class Meta:
        model = EducationArticleHeader
        fields = ['article_header_content', 'article_body_content']
    def __init__(self, *args, **kwargs):
        self.creator_id = kwargs.pop('creator_id', None)
        super(EducationArticleForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        article_header = super().save(commit=False)
        article_body_content = self.cleaned_data.get('article_body_content')
        print(self.creator_id)
        # Create a new EducationArticleBody instance

        article_body = EducationArticleBody.objects.create(article_body_content=article_body_content,creator_id=self.creator_id)
        article_header.article_body_id = article_body

        if commit:
            article_header.save()

        return article_header
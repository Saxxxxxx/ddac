from django import forms
from django.contrib import admin
from .models import EducationArticleHeader,EducationArticleBody

class EducationArticleHeaderForm(forms.ModelForm):
    article_body_content = forms.CharField(label='Article Body Content', widget=forms.Textarea, required=False)

    class Meta:
        model = EducationArticleHeader
        fields = ['article_header_content', 'article_body_content', 'creator']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.article_body_id:
            self.fields['article_body_content'].initial = instance.article_body_id.article_body_content

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit==False:
            article_body_content = self.cleaned_data.get('article_body_content')
            print(self.cleaned_data)
            if article_body_content:
                # Check if an EducationArticleBody instance exists for this header
                if instance.article_body_id:
                    article_body = instance.article_body_id
                    article_body.article_body_content = article_body_content
                    article_body.save()
                else:
                    creator_id = self.cleaned_data.get('creator')
                    # Create a new EducationArticleBody instance
                    article_body = EducationArticleBody.objects.create(article_body_content=article_body_content,creator=creator_id)
                    instance.article_body_id = article_body
            instance.save()
        return instance

@admin.register(EducationArticleHeader)
class EducationArticleHeaderAdmin(admin.ModelAdmin):
    '''DEFINE ADMIN MODEL FOR EducationArticleHeader MODEL'''
    
    list_display = ('article_header_content', 'get_article_body_content', 'creator')
    search_fields = ('article_header_content', 'article_body_id__article_body_content')
    ordering = ('article_header_content', 'creator')
    form = EducationArticleHeaderForm

    def get_article_body_content(self, obj):
        return obj.article_body_id.article_body_content if obj.article_body_id else None

    get_article_body_content.short_description = 'Article Body Content'

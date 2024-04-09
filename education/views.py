from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .forms import EducationArticleForm
from .models import EducationArticleHeader
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def education_list(request):
    return render(request,'education_list.html')

@staff_member_required
def admin_articles(request):
    headers = EducationArticleHeader.objects.all()
    educationForm = EducationArticleForm()
    if request.method == "POST":
        if 'createArticleBtn' in request.POST:
            education_article_form = EducationArticleForm(request.POST, creator_id=request.user.id)
            if education_article_form.is_valid():
                education_article = education_article_form.save(commit=False)
                education_article.creator_id = request.user.id  # Set creator_id here
                education_article.save()
                messages.success(request, 'Successful Registered.')
                return redirect('admin_articles')
        elif 'modifyArticle' in request.POST:
            article = get_object_or_404(EducationArticleHeader,pk=request.POST.get('article_id'))
            article.article_header_content = request.POST.get('title')
            if request.POST.get('title'):
                article.article_body_id.article_body_content = request.POST.get('description')
                article.article_body_id.save()
                article.save()
            else:
                article.delete()
                article.article_body_id.delete()
            messages.success(request, 'Successful Modify.')
            return redirect('admin_articles')
        elif 'deleteArticle' in request.POST:
            article = get_object_or_404(EducationArticleHeader,pk=request.POST.get('article_id'))
            article.article_body_id.delete()
            article.delete()
            messages.success(request, 'Successful deleted.')
            return redirect('admin_articles')

    

    return render(request,'admin_articles.html',{"headers":headers,"educationForm":educationForm})

def get_article(request):
    print(request.GET)
    article = EducationArticleHeader.objects.get(article_header_id=request.GET.get('article_id'))
    print(article)
    article_data = {
        'article_id':article.article_header_id,
        'article_header_content':article.article_header_content,
        'article_body_content':article.article_body_id.article_body_content,
    }
    return JsonResponse({'article_data': article_data})


from django.db import models

from account.models import User

from general.utils import *

class EducationArticleBody(AuditInfoDeleted):
    class Meta:
        db_table="education_article_body"
        
    article_body_id = models.AutoField(primary_key=True)
    article_body_content = models.TextField(blank=False,null=False)
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)


class EducationArticleHeader(AuditInfoDeleted):
    class Meta:
        db_table="education_article_header"
        
    article_header_id = models.AutoField(primary_key=True)
    article_header_content = models.CharField(max_length = 255, blank=False,null=False)
    article_body_id = models.ForeignKey(EducationArticleBody,on_delete=models.CASCADE,related_name="education_article_header_article_body",null=True)
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)
    
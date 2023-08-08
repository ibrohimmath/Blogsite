from django.db import models 
from django.urls import reverse

from django.contrib.auth import get_user_model

# from django.utils import timezone

from taggit.managers import TaggableManager

class Article(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    
    image = models.ImageField(upload_to = None)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    tags = TaggableManager()
    
    class Meta:
        ordering = ('-created_at', )
    
    def __str__(self):
        return self.title
    
    def make_short(self):
        return ' '.join(self.title.split()[:5])
    
    def display_tags(self):
        return ', '.join(list(self.tags.all().values_list('name', flat = True)))
    display_tags.short_description = 'Taglar'
    
    def get_absolute_url(self):
        return reverse('article_detail', args = [str(self.id)])
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    answer = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def children(self):
        return Comment.objects.filter(parent = self)
    
    def is_parent(self):
        if self.parent is None:
            return False
        return True 
    
    def __str__(self):
        if self.is_parent():
            return '%s dan %s ga' %(self.user, self.parent.user)
        return '%s dan \'%s\' ga kommentariya' % (self.user, self.article.make_short())            
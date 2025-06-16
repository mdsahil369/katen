from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.db.models import SlugField
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    # slug = AutoSlugField(populate_from='name',unique=True, null=True, default=None)

    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS = {
        ('0', 'DRAFT'),
        ('1', 'PUBLISH')
    }
    SECTION = {
        ('Recent', 'Recent'),
        ('Popular', 'Popular'),
        ('Trending', 'Trending')
    }


    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    # content = models.TextField()
    content = CKEditor5Field(config_name='extends')
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    blog_slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length = 1, default = 0)
    section = models.CharField(max_length=200, choices=SECTION, default='Recent')
    Main_post = models.BooleanField(default=False)

    # SEO Fields
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    # slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    meta_description = models.CharField(max_length=160, blank=True, null=True)
    meta_keywords = models.TextField(help_text="Enter one keyword per line", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.blog_slug:
            self.blog_slug = slugify(self.title)
        super().save(*args, **kwargs)
    def get_keywords_list(self):
        # Converts multiline keywords into a Python list
        return [line.strip() for line in self.meta_keywords.splitlines() if line.strip()]
    def keyword_score(self):
        # Prioritize keywords: first has highest weight
        fields_to_check = {
            'title': self.title.lower(),
            'meta_title': (self.meta_title or "").lower(),
            'meta_description': (self.meta_description or "").lower(),
            'slug': self.blog_slug.lower(),
            'content': self.content.lower(),
        }

        keywords = self.get_keywords_list()
        total_weight = 0
        max_score = 0
        matched_score = 0

        for i, kw in enumerate(keywords):
            weight = len(keywords) - i  # higher weight for earlier keywords
            max_score += weight * len(fields_to_check)
            for field_val in fields_to_check.values():
                total_weight += weight
                if kw.lower() in field_val:
                    matched_score += weight

        # Calculate percentage score
        if max_score == 0:
            return 0  # No keywords = 0%
        return int((matched_score / max_score) * 100)
    


    def __str__(self) -> str:
        return f"{self.title} ({self.category})"
    

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    blog_id = models.IntegerField(blank=True, null=True)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.post:
            self.blog_id = self.post.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.comment}"
    



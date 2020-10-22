from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from findz.utils import unique_slug_generator


class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='categories', max_length=250)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='categories', max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class Tutorial(models.Model):
    PRICING = [
        ('free', 'Free'),
        ('paid', 'Paid')
    ]

    MEDIUM = [
        ('video', 'Video'),
        ('blog', 'Blog'),
        ('book', 'Book')
    ]

    LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='tutorials', max_length=100)
    short_desc = models.TextField()
    description = RichTextField(blank=True)
    url = models.URLField()
    total_views = models.IntegerField(default=0)
    # price = models.FloatField(,blank=True)
    pricing = models.CharField(max_length=50, choices=PRICING)
    medium = models.CharField(max_length=50, choices=MEDIUM)
    level = models.CharField(max_length=50, choices=LEVEL)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    up_vote = models.ManyToManyField(User, related_name='up_vote', blank=True)
    down_vote = models.ManyToManyField(
        User, related_name='down_vote', blank=True)

    def total_up_votes(self):
        return self.up_vote.count()

    def total_down_votes(self):
        return self.down_vote.count()

    def __str__(self):
        return self.title


# class Submission(models.Model):
#     PRICING = [
#         ('free', 'Free'),
#         ('paid', 'Paid')
#     ]

#     MEDIUM = [
#         ('video', 'Video'),
#         ('blog', 'Blog'),
#         ('book', 'Book')
#     ]

#     LEVEL = [
#         ('beginner', 'Beginner'),
#         ('intermediate', 'Intermediate'),
#         ('advanced', 'Advanced')
#     ]
#     url = models.URLField()
#     text = models.TextField(max_length=200)
#     sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
#     pricing = models.CharField(max_length=50, choices=PRICING)
#     medium = models.CharField(max_length=50, choices=MEDIUM)
#     level = models.CharField(max_length=50, choices=LEVEL)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Category)
pre_save.connect(slug_generator, sender=SubCategory)
pre_save.connect(slug_generator, sender=Tutorial)

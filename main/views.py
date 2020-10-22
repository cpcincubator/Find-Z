from urllib.parse import urlparse, parse_qs
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from main.models import *
from main.serializers import SubCategorySerializer, TutorialSerializer


def index(request):
    all_category = Category.objects.all()

    context = {
        'categories': all_category
    }
    return render(request, 'main/index.html', context)


def search(request):
    if request.method == 'GET':
        query = request.GET['q']
        results = Tutorial.objects.filter(title__icontains=query)
        context = {
            'tutorials': results,
            'query': query.title()
        }
        return render(request, 'main/tutorials.html', context)


@api_view(('GET',))
def search_subcategory(request, subcategory_slug):
    if request.method == 'GET':
        query = request.GET['q']

        subcategories = SubCategory.objects.filter(category__slug=subcategory_slug).filter(title__icontains=query)
        subcategory_serializer = SubCategorySerializer(subcategories, many=True)
        return Response(subcategory_serializer.data)


@api_view(('GET',))
def course_filter(request):
    if request.method == 'GET':
        pricing = request.GET['pricing']
        medium = request.GET.getlist('medium[]')
        level = request.GET.getlist('level[]')
        query = request.GET['query']

        if '?q=' in query:
            parsed_url = urlparse(query)
            querystring = parse_qs(parsed_url.query)
            query_word = querystring['q'][0]
            tutorial_qs = Tutorial.objects.filter(title__icontains=query_word)
        else:
            parsed_url = urlparse(query)
            subcategory_slug = parsed_url.path.split('/')[-2]
            tutorial_qs = Tutorial.objects.filter(sub_category__slug=subcategory_slug)

        pricing = ['free', 'paid'] if not pricing else [pricing]
        medium = ['blog', 'video', 'book'] if not medium else medium
        level = ['beginner', 'intermediate', 'advanced'] if not level else level

        tutorials = tutorial_qs.filter(Q(pricing__in=pricing) & Q(medium__in=medium) & Q(level__in=level))

        tutorial_serializer = TutorialSerializer(tutorials, many=True)
        return Response(tutorial_serializer.data)


def category(request, category_slug):
    categories = Category.objects.filter(slug=category_slug)

    if categories.exists():
        category = categories.first()
        category_id = category.id
        all_sub_category = SubCategory.objects.filter(category_id=category_id)

        context = {
            'category': category,
            'sub_categories': all_sub_category
        }
        return render(request, 'main/categories.html', context)
    else:
        return render(request, 'main/404.html')


def sub_category(request, category_slug, sub_category_slug):
    if request.method == 'GET':
        sub_category = SubCategory.objects.filter(slug=sub_category_slug)

        if sub_category.exists():
            sub_category = sub_category.first()
            sub_category_id = sub_category.id
            all_tutorial = Tutorial.objects.filter(sub_category_id=sub_category_id)
        else:
            return render(request, 'main/404.html')

        context = {
            'sub_category': sub_category,
            'tutorials': all_tutorial,
            'category_slug': category_slug
        }
        return render(request, 'main/tutorials.html', context)

    elif request.method == 'POST':
        pricing = request.POST['pricing']
        medium = request.POST.getlist('medium[]')
        level = request.POST.getlist('level[]')

        pricing = ['free', 'paid'] if not pricing else [pricing]
        medium = ['blog', 'video', 'book'] if not medium else medium
        level = ['beginner', 'intermediate', 'advanced'] if not level else level

        tutorials = Tutorial.objects.filter(sub_category__slug=sub_category_slug).filter(Q(pricing__in=pricing) & Q(medium__in=medium) & Q(level__in=level))

        serialized_tutorials = serializers.serialize('json', tutorials, ensure_ascii=False)
        return JsonResponse(serialized_tutorials, safe=False)

def submit_tutorial(request):
    return render(request,'main/submit_tutorial.html')
    
def guidelines(request):
    return render(request,'main/guidelines.html')

def not_found(request):
    return render(request, 'main/404.html')

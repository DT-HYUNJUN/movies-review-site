from django.shortcuts import render
from django.db.models import Count
from reviews.models import Review

def review_count(request):
    # 리뷰 개수를 구합니다.
    reviews_count = Review.objects.aggregate(count=Count('id'))['count']

    context = {
        # 기존 context 변수에 추가합니다.
        'reviews_count': reviews_count
    }
    return context
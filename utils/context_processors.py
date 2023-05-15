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


def genre_dict_modal(request):
    
    genre_dict_modal = [
        '액션',
        '어드벤처',
        '애니메이션',
        '코미디',
        '범죄',
        '다큐멘터리',
        '드라마',
        '가족',
        '판타지',
        '역사',
        '공포',
        '음악',
        '미스터리',
        '로맨스',
        'SF',
        'TV',
        '스릴러',
        '전쟁',
        '서부',
    ]
    
    context = {
        'genre_dict_modal': genre_dict_modal,
    }
    return context
from django.shortcuts import render, redirect
from .models import Review, ReviewComment, Emote
from .forms import ReviewForm, ReviewCommentForm
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os
import requests
from django.http import JsonResponse

# Create your views here.

load_dotenv()
base_url = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')


@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.title = request.POST.get('title')
            form.movie = request.POST.get('movie-id')
            form.rating = request.POST.get('rating')
            form.is_spoiler = request.POST.get('is_spoiler')
            form.save()
            movie_id = request.POST.get('movie-id')
            return redirect('movies:detail', movie_id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def review_update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    movie_id = Review.objects.get(pk=review_pk).movie

    if review.user == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews:detail', movie_id, review_pk)
        else:
            form = ReviewForm(instance=review)
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'reviews/update.html', context)


@login_required
def review_delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    movie_id = review.movie

    if review.user == request.user:
        review.delete()
    return redirect('movies:detail', movie_id)


def detail(request, movie_id, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = ReviewCommentForm()
    review_comments = review.reviewcomment_set.order_by('-pk')
    review_like = Emote.objects.filter(review=review_pk, emotion=1)
    review_dislike = Emote.objects.filter(review=review_pk, emotion=0)
    review_update_form = ReviewForm(instance=review)

    liked_by_user = False
    for emote in review_like:
        if request.user == emote.user:
            liked_by_user = True
            break
    disliked_by_user = False
    for emote in review_dislike:
        if request.user == emote.user:
            disliked_by_user = True
            break


    comment_update_form_lst = []
    for comment in review_comments:
        comment_like = Emote.objects.filter(review_comment=comment.pk, emotion=1)
        comment_dislike = Emote.objects.filter(review_comment=comment.pk, emotion=0)
        comment_liked_by_user = False
        for emote in comment_like:
            if request.user == emote.user:
                comment_liked_by_user = True
                break
        comment_disliked_by_user = False
        for emote in comment_dislike:
            if request.user == emote.user:
                comment_disliked_by_user = True
                break
        comment_update_form = ReviewCommentForm(instance=comment)
        comment_update_form_lst.append((comment, comment_update_form, comment_liked_by_user, comment_disliked_by_user))

    path = f'/movie/{movie_id}'
    params = {
        'api_key': api_key,
        'language': 'ko-KR',
    }
    movie = requests.get(base_url+path, params=params).json()
    year = movie['release_date'][:4]

    context = {
        'review': review,
        'review_update_form': review_update_form,
        'review_comments': review_comments,
        'comment_form': comment_form,
        'comment_update_form_lst': comment_update_form_lst,
        'movie': movie,
        'year': year,
        'liked_by_user': liked_by_user,
        'disliked_by_user': disliked_by_user,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def comment_create(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    movie_id = review.movie
    comment_form = ReviewCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('reviews:detail', movie_id, review_pk)
    context = {
        'review': review,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def comment_update(request, review_pk, comment_pk):
    comment = ReviewComment.objects.get(pk=comment_pk)
    movie_id = Review.objects.get(pk=review_pk).movie

    if comment.user == request.user:
        if request.method == 'POST':
            comment_update_form = ReviewCommentForm(request.POST, instance=comment)
            if comment_update_form.is_valid():
                comment_update_form.save()
                return redirect('reviews:detail', movie_id, review_pk)
        else:
            comment_update_form = ReviewCommentForm(instance=comment)
    context = {
        'comment_update_form': comment_update_form,
        'comment': comment,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = ReviewComment.objects.get(pk=comment_pk)
    movie_id = Review.objects.get(pk=review_pk).movie
    if comment.user == request.user:
        comment.delete()
    return redirect('reviews:detail', movie_id, review_pk)


@login_required
def review_emote(request, review_pk, emotion):
    review = Review.objects.get(pk=review_pk)

    my_emote = Emote.objects.filter(review=review, user=request.user)
    input_emote = Emote.objects.filter(review=review, user=request.user, emotion=emotion)
    alert = False
    if my_emote.exists():
        is_checked = False
        if input_emote.exists():
            # 유저가 기존에 눌렀던 좋아요/싫어요 버튼을 다시 눌렀다면 삭제
            input_emote.delete()
        else:
            alert = True
    else:
        Emote.objects.create(review=review, user=request.user, emotion=emotion)
        is_checked = True

    cnt = Emote.objects.filter(review=review, emotion=emotion).count()
    context = {
        'is_checked': is_checked,
        'cnt': cnt,
        'alert': alert,
    }
    return JsonResponse(context)


@login_required
def comment_emote(request, review_pk, comment_pk, emotion):
    comment = ReviewComment.objects.get(pk=comment_pk)
    movie_id = Review.objects.get(pk=review_pk).movie

    my_emote = Emote.objects.filter(review_comment=comment, user=request.user)
    input_emote = Emote.objects.filter(review_comment=comment, user=request.user, emotion=emotion)
    alert = False

    if my_emote.exists():
        is_checked = False
        if input_emote.exists():
            # 유저가 기존에 눌렀던 좋아요/싫어요 버튼을 다시 눌렀다면 삭제
            input_emote.delete()
        else:
            alert = True
    else:
        Emote.objects.create(review_comment=comment, user=request.user, emotion=emotion)
        is_checked = True
    cnt = Emote.objects.filter(review_comment=comment, emotion=emotion).count()
    context = {
        'is_checked': is_checked,
        'cnt': cnt,
        'alert': alert,
    }
    return JsonResponse(context)



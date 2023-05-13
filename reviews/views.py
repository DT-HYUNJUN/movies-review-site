from django.shortcuts import render, redirect
from .models import Review, ReviewComment, Emote
from .forms import ReviewForm, ReviewCommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
# 테스트용 인덱스
def index(request):
    reviews = Review.objects.order_by('-pk')
    form = ReviewForm()
    context = {
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'reviews/index.html', context)


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
    if review.user == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews:detail', review_pk)
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
    if review.user == request.user:
        review.delete()
    return redirect('reviews:index')


def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    review_comments = review.reviewcomment_set.order_by('-pk')
    comment_form = ReviewCommentForm()
    context = {
        'review': review,
        'review_comments': review_comments,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def comment_create(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = ReviewCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('reviews:detail', review_pk)
    context = {
        'review': review,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = ReviewComment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('reviews:detail', review_pk)


@login_required
def review_emote(request, review_pk, emotion):
    review = Review.objects.get(pk=review_pk)

    my_emote = Emote.objects.filter(review=review, user=request.user)
    input_emote = Emote.objects.filter(review=review, user=request.user, emotion=emotion)

    if my_emote.exists():
        if input_emote.exists():
            # 유저가 기존에 눌렀던 좋아요/싫어요 버튼을 다시 눌렀다면 삭제
            input_emote.delete()
    else:
        Emote.objects.create(review=review, user=request.user, emotion=emotion)

    return redirect('movies:detail', review.movie)


@login_required
def comment_emote(request, review_pk, comment_pk, emotion):
    comment = ReviewComment.objects.get(pk=comment_pk)

    my_emote = Emote.objects.filter(review_comment=comment, user=request.user)
    input_emote = Emote.objects.filter(review_comment=comment, user=request.user, emotion=emotion)

    if my_emote.exists():
        if input_emote.exists():
            # 유저가 기존에 눌렀던 좋아요/싫어요 버튼을 다시 눌렀다면 삭제
            input_emote.delete()
    else:
        Emote.objects.create(review_comment=comment, user=request.user, emotion=emotion)

    return redirect('reviews:detail', review_pk)



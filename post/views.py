from django.shortcuts import render, redirect, get_object_or_404
from post.models import Tag, Follow, Post, Stream, Likes
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from userauths.models import Profile
from comments.models import Comment
# Create your views here.


def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    other_profiles = Profile.objects.all()[:15]
    liked_posts = Likes.objects.filter(user=user)
    liked_post_ids = liked_posts.values_list('post_id', flat=True)
    group_ids = posts.values_list('post_id', flat=True)
    post_items = Post.objects.filter(id__in=group_ids).order_by('-posted')
    first_comments_list = []
    count_list = []
    profile_photos = []
    for post in post_items:
        first_comment = Comment.objects.filter(post=post).first()
        comments_count = Comment.objects.filter(post=post).count()
        first_comments_list.append(first_comment)
        count_list.append(comments_count)
        profile = Profile.objects.filter(user=post.user).first()
        if profile:
            profile_photos.append(profile.image.url)
        else:
            profile_photos.append(None)
    combined_data = zip(post_items, first_comments_list,
                        count_list, profile_photos)
    context = {
        'other_profiles': other_profiles,
        'combined_data': combined_data,
        'liked_post_ids': liked_post_ids,
    }
    return render(request, 'indext.html', context)


def create_post(request):
    if request.method == 'POST':
        tag_objs = []
        picture = request.FILES.get('picture')
        caption = request.POST.get('caption')
        tags = request.POST.get('tags')
        user = request.user
        now = timezone.now()
        tag_list = tags.split(',')
        for tag in tag_list:
            t, created = Tag.objects.get_or_create(title=tag.strip())
            tag_objs.append(t)
        p = Post.objects.create(
            picture=picture,
            caption=caption,
            user=user,
            # posted=now,
            likes=0,
        )
        p.tags.set(tag_objs)
        return redirect('index')
    else:
        return render(request, 'createpost.html')


def post_details(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')
    commentcount = Comment.objects.filter(post=post).count()
    liked_posts = Likes.objects.filter(user=user)
    liked_post_ids = liked_posts.values_list('post_id', flat=True)
    if request.method == 'POST':
        body = request.POST.get('comment')
        # Create a new instance of Comment
        comment = Comment(post=post, user=user, body=body, likes=0)
        comment.save()  # Save the comment instance
        return HttpResponseRedirect(reverse('post_details', args=[post_id]))

    context = {
        'post': post,
        'comments': comments,
        'commentcount': commentcount,
        'liked_post_ids': liked_post_ids,
    }
    return render(request, 'postdetail.html', context=context)


def post_like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes+1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes-1
    post.likes = current_likes
    post.save()
    print('like saved')
    return HttpResponseRedirect(reverse('post_details', args=[post_id]))

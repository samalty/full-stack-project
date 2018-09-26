from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import RedirectView
from .models import Post
from .forms import BlogPostForm

def get_posts(request):
    """ Returns published posts within a html page """
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blogposts.html", {'posts': posts})

#def post_detail(request, pk):
def post_detail(request, slug=None):
    """ Returns a single post based on its slug """
#    post = get_object_or_404(Post, pk=pk)
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    return render(request, "postdetail.html", {'post': post})

#def create_or_edit_post(request, pk=None):
def create_or_edit_post(request, slug=None):
    """ Allows us to create or edit a blog post """
    if not request.user.is_authenticated():
        raise Http404
    else:    
#        post = get_object_or_404(Post, pk=pk) if pk else None
        post = get_object_or_404(Post, slug=slug) if slug else None
        if request.method == "POST":
            form = BlogPostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                post.user = request.user
                post.save()
                #return redirect(post_detail, post.pk)
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            form = BlogPostForm(instance=post)
        return render(request, 'blogpostform.html', {'form': form})

def delete_post(request, slug=None):
    """ Allows users to delete a blog post """
#    post = get_object_or_404(Post, pk=pk)
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect(reverse('get_posts'))

class PostLikeToggle(RedirectView):
    """ Allows user to upvote or downvote blog posts """
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url(data)
        user = self.request.user
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
        data = {
            "liked": liked
        }
        return url_
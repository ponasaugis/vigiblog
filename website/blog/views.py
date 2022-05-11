from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, DetailView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .models import BlogPost, PostComment
from .forms import PostReviewForm, CreatePostForm, EditCommentForm


# Pradžios puslapis, parodomi visi esami įrašai
class Posts(ListView):
    model = BlogPost
    context_object_name = 'blog_posts'
    paginate_by = 5
    template_name = 'index.html'
    ordering = ['-date_created']


# Įrašo detalus atvaizdavimas, bei komentaro rašymo forma
class PostDetail(DetailView, FormMixin):
    model = BlogPost
    context_object_name = 'post_detail'
    template_name = 'post.html'
    form_class = PostReviewForm



    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data(*args, **kwargs)
        context['form'] = PostReviewForm(initial={'blog_post': self.object, 'reviewer': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.blog_post = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(PostDetail, self).form_valid(form)


# Rodomi prisijungusio vartotojo įrašai
class UserPosts(LoginRequiredMixin, ListView):
    model = BlogPost
    context_object_name = 'posts'
    template_name = 'user_posts.html'

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user).order_by('-date_created')


# Įrašo kūrimas
class CreatePost(LoginRequiredMixin, CreateView):
    model = BlogPost
    success_url = '/blog'
    template_name = 'post_create.html'
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Įrašo redagavimas, gali redaguoti tik jį parašęs vartotojas
class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = CreatePostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.id})


# Įrašo trynimas, gali ištrinti tik įrašo savininkas
class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/blog'
    template_name = 'post_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Komentaro trynimas, gali ištrinti tik komentaro autorius
def delete_comment(LoginRequiredMixin, pk):
    comment = PostComment.objects.filter(id=pk)
    comment.delete()
    return redirect('/blog/post')


# Komentaro redagavimas, gali redaguoti tik komentaro autorius
class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostComment
    form_class = EditCommentForm
    template_name = 'comment_update.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.reviewer

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.blog_post_id})



# registracijos forma
@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already occupied!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with {email} already exist!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f'User {username} successfully registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

    return render(request, 'registration/register.html')


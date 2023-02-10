import socket

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeForm, PasswordChangeView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from social.models import Profile, User
# Create your views here.
from .forms import *
from .models import Social, Category, Comment
from .utils import *


# def LikeView(request, pk):
#     post = Social.objects.get(id=pk)
#     post.likes.add(request.user)
#     return HttpResponseRedirect(reverse('post', args=[str(pk)]))

@login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Social, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })


class SocialHome(DataMixin, ListView):
    model = Social
    template_name = 'social/index.html'
    context_object_name = 'posts'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Social.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Social.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'social/index.html', context=context)


def about(request):
    contact_list = Social.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'social/about.html', {"page_obj": page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'social/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST['author'] = request.user.id
        return super(AddPage, self).post(request, **kwargs)


class UpdatePostView(UpdateView):
    model = Social
    form_class = EditForm
    template_name = 'social/update_post.html'
    # fields = ['title', 'slug', 'content', 'author', 'photo', 'is_published', 'cat']


class DeletePostView(DeleteView):
    model = Social
    template_name = 'social/delete_post.html'
    success_url = reverse_lazy('home')


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'social/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


# def contact(request):
#     return HttpResponse("Обратная связь")
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'social/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Social
    template_name = 'social/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        # stuff = get_object_or_404(Social, id=self.kwargs['pk'])
        # total_likes = stuff.total_likes()
        #
        # liked = False
        # if stuff.likes.filter(id=self.request.user.id).exists():
        #     liked = True
        # context["total_likes"] = total_likes
        # context["liked"] = liked
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Social, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'social/post.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class SocialCategory(DataMixin, ListView):
    model = Social
    template_name = 'social/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Social.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
#     posts = Social.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображения по рубрикам',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'social/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'social/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'social/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = "social/edit_profile.html"
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'social/password_success.html', {})


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'social/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context


class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'social/edit_pofile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'github_url', 'insta_url']
    success_url = reverse_lazy('home')


class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "social/create_user_profile_page.html"

    # fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'social/add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('home')

from django.shortcuts import render, reverse, redirect
from django.views import generic
from .models import Post, Comment
from django.views.generic.edit import FormMixin
from .forms import CommentForm, UserUpdateForm, ProfileUpdateForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    else:
        return render(request, 'registration/register.html')


from django.db.models import Q


def search(request):
    query = request.GET.get('query')
    search_results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'search.html', {'posts': search_results, 'query': query})


class UserCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    context_object_name = "comments"
    template_name = "usercomments.html"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts.html"
    paginate_by = 5


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = "posts"
    template_name = "userposts.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = "post.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "post_form.html"
    success_url = "/"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = "/"
    template_name = "post_delete.html"
    context_object_name = 'post'

    def test_func(self):
        return self.get_object().user == self.request.user


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content']
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post', kwargs={"pk": self.kwargs['pk']})

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    # success_url = "/"
    template_name = "comment_delete.html"
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('post', kwargs={"pk": self.kwargs['post_id']})

    def test_func(self):
        return self.get_object().user == self.request.user


class UserCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse("usercomments")

    def test_func(self):
        return self.get_object().user == self.request.user


class UserCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    template_name = "comment_edit.html"
    context_object_name = 'comment'
    fields = ['content']

    def get_success_url(self):
        return reverse("usercomments")

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object().post
        form.save()
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    template_name = "comment_edit.html"
    context_object_name = 'comment'
    fields = ['content']

    def get_success_url(self):
        return reverse('post', kwargs={"pk": self.kwargs['post_id']})

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        form.save()
        return super().form_valid(form)


def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)
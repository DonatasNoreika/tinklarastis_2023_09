from django.shortcuts import render, reverse
from django.views import generic
from .models import Post
from django.views.generic.edit import FormMixin
from .forms import CommentForm

# Create your views here.
class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts.html"
    paginate_by = 5


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


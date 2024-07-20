from django.shortcuts import render,redirect
from .models import Blog
from .forms import ShareBlogForm, CommentForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView  
from django.views.generic import DetailView, FormView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class SignUpView(CreateView):
  template_name = 'users/register.html'
  success_url = reverse_lazy('login')
  form_class = CustomUserCreationForm
#   success_message = "Your profile was created successfully"

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home_page') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


# class HomePageView(ListView):
#     template_name = 'blog_templates/home_page.html'

class HomePageView(LoginRequiredMixin,ListView):
    model = Blog
    template_name = 'blog_templates/home_page.html'
    context_object_name = 'blogs'
    paginate_by = 5

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog_templates/detail_view.html' 
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        # Handle GET request
        self.object = self.get_object()
        form = ShareBlogForm()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # Handle POST request

        form = ShareBlogForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message'] + f"\n\nRead more at {request.build_absolute_uri()}"

            # Send the email
            send_mail(
                subject,
                message,
                request.user.email,
                [recipient_email],
                fail_silently=False,
            )

            messages.success(request, 'Blog post shared successfully!')
            return redirect('blog_detail', pk=self.kwargs['pk'])
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

class BlogSearchView(LoginRequiredMixin,ListView):
    model = Blog
    template_name = 'blog_templates/blog_search.html' 
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Blog.objects.filter(
            (Q(tags__name__icontains=query)))

class BlogSearchViewVector(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog_templates/blog_search.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        search_vector = SearchVector('title', 'content')
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vector, search_query)
        
        return Blog.objects.annotate(
            rank=search_rank
        ).filter(
            search_query
        ).order_by('-rank')
        
class AddCommentView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    success_url = reverse_lazy('home_page')
    template_name = 'blog_templates/add_comment.html'  


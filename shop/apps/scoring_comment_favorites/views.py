from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from apps.scoring_comment_favorites.forms import CommentForm
from .models import Comment
from apps.products.models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class CommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        comment_id = request.GET.get('comment_id')
        slug = kwargs['slug']
        initial_dict = {
            'product_id': product_id,
            'comment_id': comment_id,
        }
        form = CommentForm(initial=initial_dict)
        return render(request, 'sc-co-fa_app/create_comment.html', {'form': form, 'slug': slug})

    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        product = get_object_or_404(Product, slug=slug)

        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parent = None
            if cd["comment_id"]:
                parent_id = cd['comment_id']
                parent = Comment.objects.get(id=parent_id)

            Comment.objects.create(
                            product=product,
                            commenting_user=request.user,
                            comment_text=cd['comment_text'],
                            comment_parent=parent)

            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_details', product.slug)
        messages.error(request, 'خطا در ثبت نظر !', 'danger')
        return redirect('products:product_details', product.slug)

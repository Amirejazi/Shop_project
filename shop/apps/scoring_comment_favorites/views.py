from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from apps.scoring_comment_favorites.forms import CommentForm
from .models import Comment, Scoring,Favorite
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


def add_score(request):
    product_id = request.GET['product_id']
    score = request.GET['score']
    product = Product.objects.get(id=product_id)
    flag = Scoring.objects.filter(Q(product=product) & Q(scoring_user=request.user)).exists()
    if flag:
        Scoring.objects.filter(Q(product=product) & Q(scoring_user=request.user)).delete()
    Scoring.objects.create(
        product=product,
        scoring_user=request.user,
        score=score,
    )
    avg_score = product.get_average_score()
    return HttpResponse(avg_score)


def add_to_favorite(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    flag = Favorite.objects.filter(Q(product=product) & Q(favorite_user=request.user)).exists()
    if not flag:
        Favorite.objects.create(product=product, favorite_user=request.user)
        return HttpResponse("این کالا به لیست علاقه مندی های شما اضافه شد")
    return HttpResponse("این کالا قبلا در لیست علاقه مندی شما قرار گرفته")

def remove_from_favorite(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    flag = Favorite.objects.filter(Q(product=product) & Q(favorite_user=request.user)).exists()
    if flag:
        Favorite.objects.filter(Q(product=product) & Q(favorite_user=request.user)).delete()
        return HttpResponse("این کالا از علاقه مندی های شما حذف شد")
    return HttpResponse("این کالا قبلا از لیست علاقه مندی حذف شده")

def status_of_favorite(request):
    favorites = Favorite.objects.filter(favorite_user=request.user)
    return HttpResponse(len(favorites))


class UserFavoriteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_favorites = Favorite.objects.filter(favorite_user_id=request.user.id)
        return render(request, 'sc-co-fa_app/user_favorite.html', {'user_favorites': user_favorites})
from product.models import Category
from accounts.models import Profile


def general_context(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        parents = Category.objects.filter(parent=None) # کتگوری های اصلی
        cart_count = len(request.session.get('cart', {}))
        context = {
            'parents': parents,
            'profile': profile,
            'cart_count': cart_count
        }
    else:
        parents = Category.objects.filter(parent=None)
        context = {
            'parents': parents,
        }
    return context

from product.models import Category
from accounts.models import Profile


def general_context(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        parents = Category.objects.filter(parent=None) # کتگوری های اصلی
        context = {
            'parents': parents,
            'profile': profile,
        }
    else:
        parents = Category.objects.filter(parent=None)
        context = {
            'parents': parents,
        }
    return context

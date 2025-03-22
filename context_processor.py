from root.models import Category


def general_context(request):
    parents = Category.objects.filter(parent=None) # کتگوری های اصلی
    context = {
        'parents': parents,
    }
    return context


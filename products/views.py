from django.views.generic import ListView, DetailView

from products.models import Product, ProductCategory, ProductTag, ProductColor, Manufacture


class ProductListView(ListView):
    model = Product
    template_name = 'products/products-list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = Product.objects.filter(is_active=True).order_by('-id')

        categories = self.request.GET.getlist('cat')
        tags = self.request.GET.getlist('tag')
        colors = self.request.GET.getlist('color')
        manufactures = self.request.GET.getlist('manufacture')

        categories_id_list = []
        tags_id_list = []
        colors_id_list = []
        manufactures_id_list = []

        if categories:
            categories_id_list = list(map(int, categories[0].split(',')))
        if tags:
            tags_id_list = list(map(int, tags[0].split(',')))
        if colors:
            colors_id_list = list(map(int, colors[0].split(',')))
        if manufactures:
            manufactures_id_list = list(map(int, manufactures[0].split(',')))

        if categories_id_list:
            products = products.filter(categories__id__in=categories_id_list)
        if tags_id_list:
            products = products.filter(tags__id__in=tags_id_list)
        if colors_id_list:
            products = products.filter(colors__id__in=colors_id_list)
        if manufactures_id_list:
            products = products.filter(manufacture__id__in=manufactures_id_list)

        return products.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.filter(is_active=True, parent=None).order_by('-id')
        context["tags"] = ProductTag.objects.all().order_by('-id')
        context["colors"] = ProductColor.objects.all().order_by('-id')
        context["manufactures"] = Manufacture.objects.filter(is_active=True).order_by('-id')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["related_products"] = Product.objects.filter(
            categories__in=product.categories.values_list('id', flat=True)
        ).exclude(id=product.id).distinct()[:4]
        return context
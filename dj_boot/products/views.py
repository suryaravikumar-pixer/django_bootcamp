from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

from .forms import ProductModelForm
from .models import Product

# Create your views here.
def search_view(request, *args, **kwargs):
    # return HttpResponse("<h1>checking the Http response</h1>")
    query = request.GET.get('q') #q
    qs = Product.objects.filter(title__icontains=query[0])
    print(qs)
    context = {"name": "surya", "query": query}
    return render(request, "home.html", context)

# def product_create_view(request, *args, **kwargs):
#     print(request.POST)
#     print(request.GET)
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = ProductForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title "))
#                 title_from_input = my_form.cleaned_data.get("title")                # print("post_data", post_data)
#                 Product.objects.create(title=title_from_input)
#     return render(request, "forms.html", {})

def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Product.objects.create(**data)
        form  = ProductForm()
        # return HttpResponseRedirect("/success")
        # return redirect("/success")
    return render(request, "forms.html", {"form":form})


def product_detail_view(request, pk):
    # obj = Product.objects.get(id=id)
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404
    # try:
    #     obj = Product.objects.get(id=id)
    # except:
    #     raise Http404
    # return HttpResponse(f"Product id {obj.id}")]

    # return render (request, "products/detail.html", {"object":obj})
    return render (request, "products/detail.html", {"object":obj})

def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all() # [obj1,obj2,obj3]
    context = {"object_list" : qs}
    return render(request, "products/list.html", context)



def product_api_detail_view(request, pk, *args, **kwargs):
    # obj = Product.objects.get(id=1)
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message":"Not found"})
        
    return JsonResponse({"id":obj.id})
from django.shortcuts import render
# from django import loader

# Create your views here.


def index_fun(request):
    # html_template = loader.get_template("index.html")
    # html_context = ({})
    return render(request,"index.html")

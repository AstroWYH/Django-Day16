from django.shortcuts import render

# Create your views here.
def depart_list(request):
    """ depart list """
    return render(request, "depart_list.html")
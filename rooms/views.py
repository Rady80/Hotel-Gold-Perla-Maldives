from django.shortcuts import render

def rooms_list(request):
    return render(request, 'rooms/rooms_list.html', {})
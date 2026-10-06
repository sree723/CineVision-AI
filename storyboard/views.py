from django.shortcuts import render


def home(request):
    return render(request, "storyboard/index.html")


def input_page(request):
    return render(request, "storyboard/input.html")


def generate(request):

    if request.method == "POST":

        title = request.POST.get("title")
        genre = request.POST.get("genre")
        duration = request.POST.get("duration")
        story = request.POST.get("story")

        context = {
            "title": title,
            "genre": genre,
            "duration": duration,
            "story": story,
        }

        return render(request, "storyboard/result.html", context)

    return render(request, "storyboard/input.html")
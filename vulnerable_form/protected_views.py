from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .protected_models import XSSProtectedComment


@csrf_exempt
@require_http_methods(["GET", "POST"])
def secure_comment_view(request):
    if request.method == "POST":
        try:
            # input validation
            raw_content = request.POST.get("content", "").strip()

            # check content length
            if len(raw_content) > 1000:
                raise ValidationError("Comment too long")

            if len(raw_content) < 1:
                raise ValidationError("Comment cannot be empty")

            # create comment with sanitized content
            comment = XSSProtectedComment(content=raw_content)
            comment.save()

            return redirect("secure-comments")

        except ValidationError as e:
            print(f"error: {str(e)}")
            return redirect("secure-comments")

    # handle GET request
    comments = XSSProtectedComment.objects.all().order_by("-created_at")
    return render(request, "secure_comments.html", {"comments": comments})

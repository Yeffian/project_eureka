"""Teacher views: guest landing and (mock) signed-in dashboard.

Since this is a UI-only migration, `signed_in` is a plain context flag rather
than a real auth check. The landing page passes `signed_in=False`, the
dashboard passes `signed_in=True`; the header partial reads that to swap
between the Sign-in button and the user chip.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landing(request):
    return render(request, "teachers/landing.html", {
        "current_page": "teachers",
        "signed_in": False,
    })

@login_required(login_url='/login')
def dashboard(request):
    return render(request, "teachers/dashboard.html", {
        "current_page": "teachers",
        "signed_in": True,
        # Mock user for the header chip; wire to request.user later.
        "display_name": "Ms. Sara",
        "avatar_letter": "S",
    })

from django.shortcuts import render


# Create your views here.
def ticket_request_view(request):
    return render(request, "ticket_request/ticket_request.html")


def ticket_request_success_view(request):
    return render(request, "ticket_request/ticket_request_successed.html")

def  ticket_request_detail_view(request):
    return render(request, "ticket_request/ticket_request_detail.html")
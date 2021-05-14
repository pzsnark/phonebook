from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .utils import get_actionlog
from django.core.paginator import Paginator


@login_required()
def actionlog_view(request):
    context = get_actionlog()
    paginator = Paginator(context['all_records'], 50)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, 'actionlog/logview.html', context)

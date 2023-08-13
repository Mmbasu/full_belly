from django.shortcuts import redirect

def requires_password_change(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.check_password(request.user.temporary_password):
            return redirect('driver:settings')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

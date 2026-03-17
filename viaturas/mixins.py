from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin para restringir acesso apenas a usuários administradores."""
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect("login")
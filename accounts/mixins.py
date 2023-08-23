from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
class AdminRequiredMixin(UserPassesTestMixin):
    
    def test_func(self):
        print("In admin admin mixin")
        return self.request.user.is_authenticated and self.request.user.is_staff

class AdminLoginRequiredMixin(AdminRequiredMixin):
    print("In admin mixin")
    login_url = settings.LOGIN_URL
class ModeratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_moderator

class ModeratorLoginRequiredMixin(ModeratorRequiredMixin):
    login_url = settings.LOGIN_URL
    
class RegularUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_staff and not self.request.user.is_moderator

class RegularUserLoginRequiredMixin(RegularUserRequiredMixin):
    login_url = settings.LOGIN_URL        
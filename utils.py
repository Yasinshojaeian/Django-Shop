from datetime import datetime, timedelta
import pytz

from django.contrib.auth.mixins import UserPassesTestMixin

def send_otp_code(phone_number,code):
    print('='*90)
    print('salam')
    print(phone_number)
    print(code)


def check_expired_code(created):
    cr =  created.replace(tzinfo=None)
    test = cr + timedelta(minutes=2)
    now = datetime.now()
    if test >= now :
        return True
    return False


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
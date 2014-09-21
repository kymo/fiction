from models import Account


class MyCustomBackend:
    

    def authenticate(self, name = None, password = None):
        try:
            user = Account.objects.get(name = name)
        except Exception:
            pass

        else:
            user = Account.objects.get(name = name)
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk = user_id)
        except Exception:
            return None

from .models import SuperUserAccount, AdminAccount, InstructorAccount, StudentAccount, ParentAccount



class SuperUserAccountAuth():
    def authenticate(self, request, username, password):
        try:
            user = SuperUserAccount.objects.get(username=username)
            success = user.check_password(password)
            if success:
                return user
        except SuperUserAccount.DoesNotExist:
            pass
        return None
    
    def get_user(self, uid):
        try:
            return SuperUserAccount.objects.get(pk=uid)
        except:
            return None


class AdminAccountAuth():
    def authenticate(self, request, username, password):
        try:
            user = AdminAccount.objects.get(username=username)
            success = user.check_password(password)
            if success:
                return user
        except AdminAccount.DoesNotExist:
            pass
        return None
    
    def get_user(self, uid):
        try:
            return AdminAccount.objects.get(pk=uid)
        except:
            return None


class InstructorAccountAuth():
    def authenticate(self, request, username, password):
        try:
            user = InstructorAccount.objects.get(username=username)
            success = user.check_password(password)
            if success:
                return user
        except InstructorAccount.DoesNotExist:
            pass
        return None
    
    def get_user(self, uid):
        try:
            return InstructorAccount.objects.get(pk=uid)
        except:
            return None

class StudentAccountAuth():
    def authenticate(self, request, username, password):
        try:
            user = StudentAccount.objects.get(username=username)
            success = user.check_password(password)
            if success:
                return user
        except StudentAccount.DoesNotExist:
            pass
        return None
    
    def get_user(self, uid):
        try:
            return StudentAccount.objects.get(pk=uid)
        except:
            return None
        
class ParentAccountAuth():
    def authenticate(self, request, username, password):
        try:
            user = ParentAccount.objects.get(username=username)
            success = user.check_password(password)
            if success:
                return user
        except ParentAccount.DoesNotExist:
            pass
        return None
    
    def get_user(self, uid):
        try:
            return ParentAccount.objects.get(pk=uid)
        except:
            return None
from main.models import User


class AvatarService:
    def save(self, user: User, avatar):
        user.avatar.delete()

        user.avatar = avatar

        user.save()

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, blank = False, null=False)
    is_active = models.BooleanField(default=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True, default=None)
    unique_link_id = models.UUIDField(null=True, editable=False)
    """Reinstate following link instead of above as soon as migration completed and UUIDs forced
    # unique_link_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)"""

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.is_active = False
        instance.save()


class FriendRequest(models.Model):
    """ Friend request made from one user to another """
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_received')


class Friendship(models.Model):
    """ Friendships between two users """
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='_unused_friend_relation')

    def create_friendship(user1, user2):
        if Friendship.check_friendship(user1, user2) == False:
            friendship = Friendship(from_user=user1, to_user=user2)
            reverse_friendship = Friendship(from_user=user2, to_user=user1)
            friendship.save()
            reverse_friendship.save()
            FriendRequest.objects.filter(from_user=user1, to_user=user2).delete()
            FriendRequest.objects.filter(from_user=user2, to_user=user1).delete()

    def check_friendship(user1, user2):
        friendship = Friendship.objects.filter(from_user=user1, to_user=user2)
        reverse_friendship = Friendship.objects.filter(from_user=user2, to_user=user1)
        if friendship.count() > 0 or reverse_friendship.count() > 0:
            return True
        else:
            return False

    def list_friends(user):
        friendships = user.friends.values_list("from_user")
        friends = User.objects.filter(id__in=friendships)
        return friends

    def remove_friendship(user1, user2):
        friendship = Friendship.objects.filter(from_user=user1, to_user=user2)
        friendship.delete()
        reverse_friendship = Friendship.objects.filter(from_user=user2, to_user=user1)
        reverse_friendship.delete()

    def make_friend_request(from_user, to_user):
        """Make a friend request from one user to the other where appropriate:
        If no existing friend requests
        If friend request present the other way, make friendship instead"""
        existing_friend_requests = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
        existing_reverse_friend_requests = FriendRequest.objects.filter(from_user=to_user, to_user=from_user)
        existing_friendship = Friendship.check_friendship(from_user, to_user)

        if not existing_friendship:
            if existing_friend_requests.count() == 0:
                if existing_reverse_friend_requests.count() == 0:
                    friend_request = FriendRequest(from_user=from_user, to_user=to_user)
                    friend_request.save()
                else:
                    """Make friendship instead if there is already a reverse friend request"""
                    Friendship.create_friendship(from_user, to_user)

    def check_friend_request_exists(from_user, to_user):
        return FriendRequest.objects.filter(from_user=from_user, to_user=to_user).count() > 0

    def reject_friend_request(from_user, to_user):
        """Reject all pending friend requests from other user"""
        existing_friend_requests = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
        existing_friend_requests.delete()
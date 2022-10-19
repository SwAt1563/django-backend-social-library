from friend.models import UserFollowing
import pytest



@pytest.mark.django_db
def test_unfollow_user(auth_client, user, admin):
    follow_object = UserFollowing.objects.create(user_id=user, following_user_id=admin)

    payload = dict(
        user_id=user.id,
        following_user_slug=admin.profile.slug,
    )

    response = auth_client.delete('/friend/unfollow/', payload)

    with pytest.raises(UserFollowing.DoesNotExist):
        follow_object.refresh_from_db()
    assert response.status_code == 204

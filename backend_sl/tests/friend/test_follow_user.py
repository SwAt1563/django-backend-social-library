from friend.models import UserFollowing
import pytest



@pytest.mark.django_db
def test_follow_user(auth_client, user, admin):

    payload = dict(
        user_id=user.id,
        following_user_slug=admin.profile.slug,
    )

    response = auth_client.post('/friend/follow/', payload)

    follow_object = UserFollowing.objects.filter(user_id=user, following_user_id=admin).get()
    assert response.status_code == 201
    assert follow_object is not None

@pytest.mark.django_db
def test_duplicated_follow_user(auth_client, user, admin):
    UserFollowing.objects.create(user_id=user, following_user_id=admin)
    payload = dict(
        user_id=user.id,
        following_user_slug=admin.profile.slug,
    )

    response = auth_client.post('/friend/follow/', payload)

    assert response.status_code == 400

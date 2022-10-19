import pytest
from friend.models import UserFollowing



@pytest.mark.django_db
def test_get_followers(auth_client, user, admin):
    UserFollowing.objects.create(user_id=user, following_user_id=admin)
    payload = dict(
        user_id=user.id,
        related_user_slug=admin.profile.slug,
    )

    response = auth_client.get('/friend/followers/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['profile_slug'] == user.profile.slug


@pytest.mark.django_db
def test_get_followers_with_filter(auth_client, user, admin):
    UserFollowing.objects.create(user_id=user, following_user_id=admin)
    payload = dict(
        user_id=user.id,
        related_user_slug=admin.profile.slug,
        filter='no any',
    )

    response = auth_client.get('/friend/followers/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 0

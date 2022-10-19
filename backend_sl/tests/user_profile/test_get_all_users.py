import pytest



@pytest.mark.django_db
def test_get_all_users(auth_client, admin, user):
    payload = dict(
        user_id=user.id,
    )

    response = auth_client.get('/profile/all_users/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 2


@pytest.mark.django_db
def test_get_all_users_with_filter(auth_client, admin, user):
    payload = dict(
        user_id=user.id,
        filter='user',
    )

    response = auth_client.get('/profile/all_users/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['profile_slug'] == user.profile.slug

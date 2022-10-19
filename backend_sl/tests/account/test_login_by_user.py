import pytest



@pytest.mark.django_db
def test_login_user(client, user):
    user_data = dict(
        username=user.username,
        email=user.email,
        user_id=user.id,
        is_admin=user.is_admin,
        profile_slug=user.profile.slug
    )
    payload = dict(
        email=user.email,
        password='1',
    )
    response = client.post('/account/token_by_email/', payload)
    data = response.data

    assert 'access' in data
    assert 'refresh' in data
    assert user_data['username'] == data['username']
    assert user_data['email'] == data['email']
    assert user_data['user_id'] == data['user_id']
    assert user_data['is_admin'] == data['is_admin']
    assert user_data['profile_slug'] == data['profile_slug']

@pytest.mark.django_db
def test_refresh_token(client, user):
    payload = dict(
        email=user.email,
        password='1',
    )
    response = client.post('/account/token_by_email/', payload)
    data = response.data

    refresh = data['refresh']

    new_access_token_response = client.post('/account/token/refresh/', {'refresh': refresh})
    new_data = new_access_token_response.data

    assert 'access' in new_data





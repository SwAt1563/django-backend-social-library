import pytest



@pytest.mark.django_db
def test_login_admin(client, admin):
    admin_data = dict(
        username=admin.username,
        email=admin.email,
        user_id=admin.id,
        is_admin=admin.is_admin,
        profile_slug=admin.profile.slug
    )
    payload = dict(
        username=admin.username,
        password='1',
    )
    response = client.post('/account/token/', payload)
    data = response.data

    assert 'access' in data
    assert 'refresh' in data
    assert admin_data['username'] == data['username']
    assert admin_data['email'] == data['email']
    assert admin_data['user_id'] == data['user_id']
    assert admin_data['is_admin'] == data['is_admin']
    assert admin_data['profile_slug'] == data['profile_slug']


@pytest.mark.django_db
def test_login_user_fail(client, user):
    payload = dict(
        username=user.username,
        password='1',
    )
    response = client.post('/account/token/', payload)

    assert response.status_code == 403


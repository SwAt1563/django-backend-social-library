import pytest

@pytest.mark.django_db
def test_update_user_profile(auth_client, user):
    profile_slug = user.profile.slug
    payload = {
        'user_id': user.id,
        # when use nested serializer we should access like this -object.inner-
        'user.first_name': 'Qutaiba',
        'user.last_name': 'Olayyan',
        'age': 22,
    }

    response = auth_client.put(f'/profile/p/{profile_slug}/', payload)
    data = response.data

    user.refresh_from_db()

    assert response.status_code == 200
    assert data['profile_slug'] == profile_slug
    assert data['age'] == user.profile.age
    assert data['user']['first_name'] == user.first_name
    assert data['user']['last_name'] == user.last_name
    assert data['user']['email'] == user.email
    assert data['user']['full_name'] == user.get_full_name == 'Qutaiba Olayyan'


@pytest.mark.django_db
def test_update_user_profile_not_owner(auth_admin_client, admin, user):
    profile_slug = user.profile.slug
    payload = {
        'user_id': admin.id,
        # when use nested serializer we should access like this -object.inner-
        'user.first_name': 'Qutaiba',
        'user.last_name': 'Olayyan',
        'age': 22,
    }

    response = auth_admin_client.put(f'/profile/p/{profile_slug}/', payload)

    # no permission
    assert response.status_code == 403


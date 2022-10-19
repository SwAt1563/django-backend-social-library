import pytest



@pytest.mark.django_db
def test_retrieve_user_profile(auth_client, user):
    profile_slug = user.profile.slug
    payload = dict(
        user_id=user.id,
    )

    response = auth_client.get(f'/profile/p/{profile_slug}/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['profile_slug'] == profile_slug


@pytest.mark.django_db
def test_retrieve_user_profile_not_owner(auth_admin_client, admin, user):
    profile_slug = user.profile.slug
    payload = dict(
        user_id=admin.id,
    )

    response = auth_admin_client.get(f'/profile/p/{profile_slug}/', payload)

    # any user can see the profile so he has permission
    assert response.status_code == 200



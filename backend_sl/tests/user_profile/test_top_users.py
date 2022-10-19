import pytest



@pytest.mark.django_db
def test_get_top_three_users(auth_client, admin, user):
    payload = dict(
        user_id=user.id,
    )

    response = auth_client.get('/profile/top_users/', payload)
    data = response.data

    assert response.status_code == 200   
    assert data['count'] == 2

import pytest
from account.models import UserAccount

@pytest.mark.django_db
def test_reset_password(client, user):
    payload = dict(
        email=user.email,
        question=user.question,
        answer=user.answer,
    )

    response = client.post('/account/reset_password_token/', payload)
    data = response.data

    assert 'reset_password_token' in data

# @pytest.mark.django_db
# def test_change_password(client, user):
#
#     old_password = user.password
#     payload = dict(
#         email=user.email,
#         question=user.question,
#         answer=user.answer,
#     )
#     response = client.post('/account/reset_password_token/', payload)
#     data = response.data
#
#     reset_password_token = data['reset_password_token']
#     new_password = 'aasfsgsdgsdgsd15566'
#
#     payload = dict(
#         reset_password_token=reset_password_token,
#         new_password=new_password,
#
#     )
#
#     # this will not update the current user
#     # it will update the user in the data base
#     response = client.post('/account/change_password/', payload)
#
#
#     # cuz just one user we have in testing
#     get_user_from_db = UserAccount.objects.all().first()
#     new_user_password = get_user_from_db.password
#
#     assert response.status_code == 200
#     assert new_user_password != old_password


@pytest.mark.django_db
def test_change_password2(client, user):

    old_password = user.password
    payload = dict(
        email=user.email,
        question=user.question,
        answer=user.answer,
    )
    response = client.post('/account/reset_password_token/', payload)
    data = response.data

    reset_password_token = data['reset_password_token']
    new_password = 'aasfsgsdgsdgsd15566'

    payload = dict(
        reset_password_token=reset_password_token,
        new_password=new_password,

    )


    response = client.post('/account/change_password/', payload)

    # for get the updated user from the database
    user.refresh_from_db()
    new_user_password = user.password

    assert response.status_code == 200
    assert new_user_password != old_password





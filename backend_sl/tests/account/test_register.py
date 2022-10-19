import pytest
from account.models import UserAccount


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        username='qutaibaa',
        password='qutaibaolayyan123+-*/',  # write only
        password2='qutaibaolayyan123+-*/',
        email='1190780@student.birzeit.edu',
        question='q',
        answer='a',
    )

    response = client.post('/account/register/', payload)
    data = response.data

    new_user = UserAccount.objects.all().first()

    assert new_user is not None
    assert new_user.profile is not None
    assert new_user.username == payload['username']
    assert data['username'] == payload['username']
    assert data['email'] == payload['email']
    assert data['question'] == payload['question']
    assert data['answer'] == payload['answer']
    assert 'password' not in data and 'password2' not in data


@pytest.mark.django_db
@pytest.mark.parametrize("test_email",
                         [
                             "qq@student.birzeit.edu",
                             "11@student.birzeit.edu",
                             "1190760@studen.birzeit.edu",
                             "1190760@student.birzoit.edu",
                             "1190760@student.birzoit.com"
                         ])
def test_register_email_wrong_format_fail(client, test_email):
    payload = dict(
        username='qutaibaa',
        password='qutaibaolayyan123+-*/',  # write only
        password2='qutaibaolayyan123+-*/',
        email=test_email,
        question='q',
        answer='a',
    )

    response = client.post('/account/register/', payload)

    assert response.status_code == 400


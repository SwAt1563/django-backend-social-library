from rest_framework.test import APIClient
import pytest
from account.models import UserAccount
from post.models import Post


# if i want to  use the available database of the project
# @pytest.fixture(scope='session')
# def django_db_setup():
#     from django.conf import settings
#     settings.DATABASES['test_db'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db_name.sqlite3',
#     }

@pytest.fixture
def user():
    user = UserAccount(username='user',
                       email='1190760@student.birzeit.edu',
                       question='a',
                       answer='b')
    user.set_password('1')
    # this save also will make profile for this user
    user.save()
    return user


@pytest.fixture
def admin():
    admin = UserAccount(username='admin',
                        email='1190761@student.birzeit.edu',
                        question='aa',
                        answer='bb',
                        is_admin=True)
    admin.set_password('1')
    # this save also will make profile for this admin
    admin.save()

    return admin


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    payload = dict(
        email=user.email,
        password='1',
    )
    response = client.post('/account/token_by_email/', payload)
    data = response.data
    access_token = data['access']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    return client

@pytest.fixture
def auth_admin_client(admin, client):
    payload = dict(
        username=admin.username,
        password='1',
    )
    response = client.post('/account/token/', payload)
    data = response.data
    access_token = data['access']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')


    return client


@pytest.fixture
def un_active_post(auth_client, user):
    try:
        file_path = 'tests/files/University Library.pdf'
        file = open(file_path, 'rb')
        files = {'file': file}

        payload = dict(
            title='test_post',
            description='Just for testing',
            file=file,
            user_id=user.id,
        )

        response = auth_client.post('/post/post_create/', payload, format='multipart', files=files)
    finally:
        file.close()

    post = Post.objects.get(title=payload['title'])

    return post


@pytest.fixture
def active_post(un_active_post):
    post = un_active_post
    post.status = 'COMPLETED'
    post.save()
    post.refresh_from_db()
    return post

@pytest.fixture
def active_posts(active_post):

    for i in range(1, 4):
        Post.objects.create(title=f'{active_post.title}_{i}',
                            description=f'{active_post.description}_{i}',
                            file=active_post.file,
                            user=active_post.user,
                            status=active_post.status)

    active_post.delete()
    return Post.objects.all()


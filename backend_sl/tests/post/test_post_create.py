import pytest
from post.models import Post




@pytest.mark.django_db
def test_create_post(auth_client, user):

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

    # 201: created success

    assert response.status_code == 201
    assert post.title == payload['title']
    assert post.description == payload['description']
    assert hasattr(post, 'file')



@pytest.mark.django_db
@pytest.mark.parametrize("filename",
                         [
                             "Me.jpg",
                             "Me.png",
                             "University Library.pdf",
                         ])
def test_create_post_correct_format(auth_client, user, filename):
    try:
        file_path = f'tests/files/{filename}'
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

    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize("filename",
                         [
                             "q.txt",
                             "ADfa.yml",
                         ])
def test_create_post_wrong_format(auth_client, user, filename):
    try:
        file_path = f'tests/files/{filename}'
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

    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(title='test_post')

    assert response.status_code == 400

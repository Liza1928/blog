import pytest
from rest_framework.exceptions import ValidationError
from blog.models import Category


@pytest.mark.usefixtures('create_category')
@pytest.mark.django_db
class TestCategoryModel:

    def test_create(self):
        Category.objects.create(name='name')
        assert Category.objects.get(name='name').name == 'name'

    def test_unique_name(self):
        with pytest.raises(ValidationError):
            Category.objects.create(name='name1')

    def test_update(self):
        category = Category.objects.get(name='name1')
        category.name = 'test_name'
        category.save()
        assert Category.objects.get(name='test_name').name == 'test_name'

    def test_delete(self):
        row_num, _ = self.category1.delete()
        assert row_num == 1

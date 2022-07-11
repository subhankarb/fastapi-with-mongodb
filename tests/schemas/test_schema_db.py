import datetime

import pytest
from bson.errors import InvalidId
from hamcrest import *

from app.schemas.schema_db import ToDoCategoryInDB, PyObjectId


class TestToDOItemInDB:

    @pytest.mark.parametrize(
        "category_id", [
            ("1233",),
            ("foo-bar-quux",),
            ("666f6f2d6261722d71757578",)
        ])
    def test_invalid_category_id_check(self, category_id):
        with pytest.raises(TypeError) as excinfo:
            obs = ToDoCategoryInDB(id=PyObjectId(category_id), category_name="testing",
                                   created_at=datetime.datetime.utcnow())
            assert_that(excinfo, is_(InvalidId))

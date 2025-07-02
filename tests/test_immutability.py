#-------------------- Imports --------------------

from src.Stash import Stash
from src.Stash.Errors.exceptions import FreezeAttributeException

import pytest

#-------------------- Testing Immutability --------------------

def test_immutable_variables():

    @Stash(freeze=True)
    class TestExample():
        name: str
        age: int
        is_villain: bool

    example1 = TestExample(
        name="Steve Rogers",
        age=50,
        is_villain=False
    )

    assert example1.name == "Steve Rogers"
    assert example1.age == 50
    assert example1.is_villain is False

    with pytest.raises(FreezeAttributeException):
        example1.age = 100

if __name__ == "__main__":
    pytest.main()






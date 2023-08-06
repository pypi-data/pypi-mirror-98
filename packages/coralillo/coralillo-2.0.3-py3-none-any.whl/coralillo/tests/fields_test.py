from coralillo import Model, datamodel
from coralillo.hashing import check_password, make_password
from coralillo.fields import Text, Location, Hash, Bool, MissingFieldError
from coralillo.fields import Integer, InvalidFieldError, Float, Datetime, Dict
from datetime import datetime
import time
import os
import pytest

from .models import Truck, User, Subscription

os.environ['TZ'] = 'UTC'
time.tzset()


def test_field_text():
    field = Text(name='field', default='pollo')

    assert field.recover(None, {'field': 'foo'}, 'field') == 'foo'
    assert field.prepare('foo') == 'foo'
    assert field.validate(None, None, 'field') == 'pollo'
    assert field.recover(None, {'field': ''}, 'field') == ''
    assert field.recover(None, {'field': None}, 'field') is None
    assert field.recover(None, {'field': 'None'}, 'field') is None


def test_field_text_validate():
    field = Text(name='field')

    with pytest.raises(MissingFieldError):
        field.validate(None, '', None)


def test_field_hash():
    field = Hash(name='field')

    assert field.recover(None, {'field': 'foo'}, 'field') == 'foo'
    assert field.validate(None, 'foo', 'field') != 'foo'
    assert field.recover(None, {'field': None}, 'field') is None
    assert field.recover(None, {'field': 'None'}, 'field') is None


def test_field_bool():
    field = Bool(name='field')

    assert field.recover(None, {'field': 'True'}, 'field') is True
    assert field.recover(None, {'field': 'False'}, 'field') is False
    assert field.prepare(True) == 'True'
    assert field.prepare(False) == 'False'
    assert field.recover(None, {'field': None}, 'field') is None
    assert field.recover(None, {'field': 'None'}, 'field') is None

    assert field.validate(None, 'true', 'field') is True
    assert field.validate(None, 'false', 'field') is False
    assert field.validate(None, '1', 'field') is True
    assert field.validate(None, '0', 'field') is False
    assert field.validate(None, '', 'field') is False


def test_field_int():
    field = Integer(name='field')

    assert field.recover(None, {'field': '35'}, 'field') == 35
    assert field.recover(None, {'field': '0'}, 'field') == 0
    assert field.recover(None, {'field': ''}, 'field') is None
    assert field.recover(None, {'field': None}, 'field') is None
    assert field.recover(None, {'field': 'None'}, 'field') is None

    assert field.prepare(35) == '35'
    assert field.prepare(0) == '0'

    assert field.validate(None, 0, 'field') == 0
    assert field.validate(None, '0', 'field') == 0

    with pytest.raises(MissingFieldError):
        field.validate(None, '', 'field')

    with pytest.raises(InvalidFieldError):
        field.validate(None, 'pollo', 'field')


def test_field_int_no_required():
    field = Integer(name='field', required=False)

    assert field.validate(None, None, 'field') is None
    assert field.validate(None, '', 'field') is None


def test_field_float():
    field = Float(name='field')

    assert field.recover(None, {'field': '3.14'}, 'field') == 3.14
    assert field.recover(None, {'field': '0'}, 'field') == 0.0
    assert field.recover(None, {'field': ''}, 'field') is None
    assert field.recover(None, {'field': None}, 'field') is None
    assert field.recover(None, {'field': 'None'}, 'field') is None

    assert field.prepare(3.14) == '3.14'
    assert field.prepare(0.0) == '0.0'

    assert field.validate(None, 0, 'field') == 0
    assert field.validate(None, '0', 'field') == 0


def test_field_date():
    field = Datetime(name='field')

    assert field.recover(None, {'field': '1499794899'}, 'field') == datetime(2017, 7, 11, 17, 41, 39)
    assert field.recover(None, {'field': ''}, 'field') is None
    assert field.recover(None, {'field': None}, 'field') is None
    assert field.recover(None, {'field': 'None'}, 'field') is None
    assert field.prepare(datetime(2017, 7, 11, 17, 41, 39)) == '1499794899'


def test_field_location(nrm):
    class MyModel(Model):
        field = Location()

        class Meta:
            engine = nrm

    obj = MyModel(field=datamodel.Location(-103.3590, 20.7240)).save()

    assert nrm.redis.type('my_model:geo_field') == b'zset'
    assert MyModel.get(obj.id).field == datamodel.Location(-103.3590, 20.7240)


def test_field_location_validate(nrm):
    class MyModel(Model):
        field = Location()

        class Meta:
            engine = nrm

    item = MyModel.validate(field='-100,20').save()
    assert item.field == datamodel.Location(-100, 20)

    item_rec = MyModel.get(item.id)
    assert item_rec.field == datamodel.Location(-100, 20)


def test_field_location_none(nrm):
    class MyModel(Model):
        field = Location(required=False)

        class Meta:
            engine = nrm

    item = MyModel.validate().save()

    item_rec = MyModel.get(item.id)

    assert item_rec.field is None


def test_password_check():
    user = User(
        password=make_password('123456'),
    ).save()

    assert check_password('123456', user.password)
    assert user.password != '123456'


def test_empty_field_dict(nrm):
    class Dummy(Model):
        dynamic = Dict()

        class Meta:
            engine = nrm

    a = Dummy().save()
    loaded_a = Dummy.get(a.id)

    assert loaded_a.dynamic == {}


def test_field_dict(nrm):
    class Dummy(Model):
        name = Text()
        dynamic = Dict()

        class Meta:
            engine = nrm

    # Create and save models with a dict field
    a = Dummy(
        name='dummy',
        dynamic={
            '1': 'one',
        },
    ).save()

    b = Dummy(
        name='dummy',
        dynamic={
            '2': 'two',
        },
    ).save()

    c = Dummy(
        name='dummy',
        dynamic={
            '1': 'one',
            '2': 'two',
        },
    ).save()

    # override dict
    a.dynamic = {
        '3': 'thre',
    }

    a.save()

    loaded_a = Dummy.get(a.id)
    loaded_b = Dummy.get(b.id)
    loaded_c = Dummy.get(c.id)

    assert a.dynamic == loaded_a.dynamic
    assert b.dynamic == loaded_b.dynamic
    assert c.dynamic == loaded_c.dynamic


def test_field_position_delete():
    c1 = Truck(last_position=datamodel.Location(-90, 21)).save()
    c2 = Truck(last_position=datamodel.Location(-90, 22)).save()

    assert Truck.get(c1.id).last_position == datamodel.Location(-90, 21)
    assert Truck.get(c2.id).last_position == datamodel.Location(-90, 22)

    c1.delete()

    assert Truck.get(c1.id) is None

    assert Truck.get(c2.id).last_position == datamodel.Location(-90, 22)


def test_tree_index():
    Subscription(key_name='a:b:c:d').save()
    s1 = Subscription(key_name='a:b:c').save()
    s2 = Subscription(key_name='a:b').save()
    s3 = Subscription(key_name='a').save()

    assert Subscription.tree_match('key_name', 'a:b:c') == [s1, s2, s3]

    s3.delete()
    assert Subscription.tree_match('key_name', 'a:b:c') == [s1, s2]

    s2.delete()
    assert Subscription.tree_match('key_name', 'a:b:c') == [s1]

    s1.delete()
    assert Subscription.tree_match('key_name', 'a:b:c') == []

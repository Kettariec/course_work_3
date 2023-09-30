import os
from main import list_of_classes, load_payments, Payment
payments_path = os.path.join("data", "operations.json")
all_payments = load_payments(payments_path)


def test_list_of_classes():
    data = list_of_classes(all_payments)
    assert isinstance(data, list)


def test_load_payments():
    data = load_payments(payments_path)
    assert isinstance(data, list)


def test_class_payment():
    res = Payment("EXECUTED", "2019-08-26T10:50:58.294041", "Перевод организации", "Maestro 1596837868705199", "Счет 64686473678894779589", "31957.58", "руб.")
    assert res.from_is_correct() == "Maestro 1596 83** **** 5199"
    assert res.to_correct() == "Счет **9589"
    assert res.result() == "2019.08.26 Перевод организации\nMaestro 1596 83** **** 5199 -> Счет **9589\n31957.58 руб.\n"

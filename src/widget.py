def mask_account_card(number: str) -> str:
    """Функция принимает на вход номер карты и счета и возвращает их маску, номер карты и номер счета замаскирован."""
    card_number = ""
    name_card = ""
    if "счёт" in number.lower() or "счет" in number.lower():
        if len(number) != 25:
            return "Error"
        for num in number[5:]:
            if num.isalpha():
                return "Error"
        else:
            score_number = number[5:]
            number_mask = number[0:4] + " " + "**" + score_number[-4:]
            return number_mask
    else:
        for num in number:
            if num.isalpha() or num == " ":
                name_card += num
            else:
                card_number += num
        if len(card_number) < 16:
            return "Error"
        for card_num in card_number:
            if card_num.isalpha():
                return "Error"
        else:

            correct_number = card_number[0:7] + card_number[7:14] + card_number[14:19]
            number_mask = (
                name_card
                + correct_number[0:4]
                + " "
                + correct_number[4:6]
                + "**"
                + " "
                + "****"
                + " "
                + correct_number[12:16]
            )

            return number_mask


def get_date(date: str) -> str:
    """Функция принимает на вход строку и отдает корректный результат в формате 11.07.2018."""

    # Проверяем, есть ли точка после секунд
    if '.' in date and date.endswith('.'):
        return "Error"

    # Далее продолжаем обработку, как раньше
    if len(date) < 10 or len(date) > 26:
        return "Error"

    try:
        day = date[8:10]
        month = date[5:7]
        year = date[0:4]
        correct_date = f"{day}.{month}.{year}"
        return correct_date
    except IndexError:
        return "Error"

def generate_variants(item_count: list) -> list:
    return [chr(ord('a') + i) for i in range(len(item_count))]


def translator(sentence_uz, sentence_ru, language) -> str:
    return sentence_uz if language == 'uz' else sentence_ru


def checking_solved_tests_format(tests, language):
    message = ""

    for index, test in enumerate(tests, start=1):
        variants = generate_variants(test['variants_uz'])

        message += f"{index}. {test[f'question_{language}']}\n"

        for test_variant, variant in zip(test[f'variants_{language}'], variants):
            text = f'{variant.upper()}. {test_variant}\n'

            if test_variant == test[f'correct_answer_{language}']:
                text = f'{variant.upper()}. {test_variant} ✅\n'

            if test_variant == test[f'answer_{language}'] and test[f'answer_{language}'] != test[f'correct_answer_{language}']:
                text = f'{variant.upper()}. {test_variant} ➖\n\n'

            message += text

    return message

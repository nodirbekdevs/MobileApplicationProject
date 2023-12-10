from fastapi import Request, UploadFile
from typing import List
from random import sample
from asyncio import to_thread
from base64 import b64decode
from io import BytesIO
from json import dumps

from .user import UserController
from ..models import Test, Section
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, Filter, Translator, File, Populate
from ..utils import INSTRUCTOR, TEST, uploads_file_path


class TestController:
    def __init__(self):
        self.repo: CoreRepository = Storage.test
        self.response = SendResponse

    async def get_all(self, request, user):
        params = request.query_params

        query = dict()

        if user['role'] == INSTRUCTOR:
            query.update(instrucor_id=user['id'])

        filtered: dict = Filter(query=query).filtering_with_params(params=params)

        tests: List[Test] = await self.repo.list(query=filtered, populate=Populate.test)

        data = Pagination(params=params, datas=tests, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        test: Test = await self.repo.retrieve(query=query, populate=Populate.test)

        if test is None:
            return self.response.failure(
                data=dict(message=f'Test with this {query} query does not exists'), status_code=404
            )

        return self.response.success(data=self.repo.schemas.retrieve(test), status_code=200)

    async def get_for_solving(self, query):
        tests = await Storage.test.list(query=dict(section_id=int(query['section_id'])))

        if len(tests) < 3:
            return self.response.failure(data=dict(message='Not enough tests for performance'), status_code=400)

        returning_tests = [test.id for test in sample(tests, 3)]

        return self.response.success(data=dict(tests=returning_tests), status_code=200)

    async def check(self, user, data: dict):
        entering_user = await UserController(user_id=user['id'], user_type=user['role']).get_one()

        number_unsolved_tests, number_solved_tests, checked_solved_tests = 0, 0, []

        language = 'ru' if entering_user.lang == 'uz' else 'uz'

        statistic_data = dict(student_id=user['id'])

        test: dict = dict()

        for solved_test in data['tests']:
            for key, item in solved_test.items():
                test: Test = await self.repo.retrieve(query=dict(id=int(key)))

                new_test = test.to_dict(exclude=['is_active', 'updated_at', 'created_at', 'image'])
                new_test.update(
                    instructor_id=test.instructor_id.id, subject_id=test.subject_id.id, section_id=test.section_id.id
                )

                translated_answer = await Translator(language=language).translate(text=item)

                if entering_user.lang == 'uz':
                    new_test.update(answer_uz=item, answer_ru=translated_answer)
                elif entering_user.lang == 'ru':
                    new_test.update(answer_uz=translated_answer, answer_ru=item)

                checked_solved_tests.append(new_test)

                if item in [test.correct_answer_uz, test.correct_answer_ru]:
                    number_solved_tests += 1
                else:
                    number_unsolved_tests += 1

        percentage = (number_solved_tests / len(data['tests'])) * 100

        returning_data = dict(
            checked_tests=dumps(checked_solved_tests),
            total_tests=len(data['tests']),
            right_count=number_solved_tests,
            wrong_count=number_unsolved_tests,
            percentage=percentage,
            solved_time=data['time']
        )

        statistic_data.update(
            instructor_id=test.instructor_id,
            subject_id=test.subject_id,
            section_id=test.section_id,
            **returning_data
        )

        await Storage.statistics.create_not_schemas(data=statistic_data)

        return self.response.success(data=returning_data, status_code=201)

    async def create(self, user, data: dict, file):
        user = await UserController(user_id=user['id'], user_type=user['role']).get_one()

        language = 'ru' if user.lang == 'uz' else 'uz'

        translator = Translator(language=language)

        translated_question = await translator.translate(text=data['question'])
        translated_variants = []
        for variant in data['variants']:
            translated_variant = await translator.translate(text=variant)
            translated_variants.append(translated_variant)
        translated_correct_answer = await translator.translate(text=data['correct_answer'])

        test_data = dict(
            instructor_id=data['instructor'], subject_id=data['subject'], section_id=data['section']
        )

        test_data.update(
            question_uz=translated_question, question_ru=data['question'],
            variants_uz=translated_variants, variants_ru=data['variants'],
            correct_answer_uz=translated_correct_answer, correct_answer_ru=data['correct_answer']
        ) if language == 'uz' else test_data.update(
            question_uz=data['question'], question_ru=translated_question,
            variants_uz=data['variants'], variants_ru=translated_variants,
            correct_answer_uz=data['correct_answer'], correct_answer_ru=translated_correct_answer
        )

        if file:
            decoded_bytes = await to_thread(b64decode, file)

            image = UploadFile(BytesIO(decoded_bytes))

            file_path: str = await File(file=image).save(
                file_model_type=TEST, path=uploads_file_path, title=data['question']
            )

            test_data.update(image=file_path)

        section: Section = await Storage.section.retrieve(query=dict(id=data['section']))
        section.total_tests += 1
        await section.update()

        test: Test = await self.repo.create(data=test_data)

        return self.response.success(data=test, status_code=201)

    async def update(self, user, query: dict, data: dict, file):
        test: Test = await self.repo.retrieve(query=query)

        if test is None:
            return self.response.failure(
                data=dict(message=f'Test with this {query} query does not exists'), status_code=404
            )

        user = await UserController(user_id=user['id'], user_type=user['role']).get_one()

        language = 'ru' if user.lang == 'uz' else 'uz'

        translator = Translator(language=language)

        test_query, test_data = dict(), dict()

        if data.get('question'):
            translated_question = await translator.translate(data['question'])

            test_query.update(section_id=test.section_id.id)

            test_query = test_query.update(question_uz=data['question']) \
                if language == 'ru' else \
                test_query.update(question_ru=translated_question)

            test_data.update(
                question_uz=translated_question, question_ru=data['question']
            ) if language == 'uz' else test_data.update(
                question_uz=data['question'], question_ru=translated_question
            )

        if test_query:
            test: Test = await self.repo.retrieve(query=test_query)

            if test:
                return self.response.failure(
                    status_code=400, data=dict(message="Test with this question already exists!")
                )

        if data.get('variants'):
            updating_variants = data['variants']

            if type(updating_variants) is dict:
                exact_variant_uz = test.variants_uz[updating_variants['index']]

                variant = await translator.translate(text=updating_variants['text'])

                inserting_variant_index = updating_variants['index'] + 1

                if user.lang == 'uz':
                    test.variants_uz.insert(inserting_variant_index, updating_variants['text'])
                    test.variants_ru.insert(inserting_variant_index, variant)
                if user.lang == 'ru':
                    test.variants_uz.insert(inserting_variant_index, variant)
                    test.variants_ru.insert(inserting_variant_index, updating_variants['text'])

                test.variants_uz.pop(updating_variants['index'])
                test.variants_ru.pop(updating_variants['index'])

                updated_variants_uz, updated_variants_ru = test.variants_uz, test.variants_ru

                test_data.update(variants_uz=updated_variants_uz, variants_ru=updated_variants_ru)

                if exact_variant_uz == test.correct_answer_uz:
                    test_data.update(correct_answer_uz=updating_variants['text'], correct_answer_ru=variant) \
                        if user.lang == 'uz' else \
                        test_data.update(correct_answer_uz=variant, correct_answer_ru=updating_variants['text'])

            elif type(updating_variants) is list:
                updated_variants_uz, updated_variants_ru = [], []

                for updating_variant in updating_variants:
                    exact_variant_uz = test.variants_uz[updating_variant['index']]

                    variant = await translator.translate(text=updating_variant['text'])

                    inserting_variant_index = updating_variants['index'] + 1

                    if user.lang == 'uz':
                        test.variants_uz.insert(inserting_variant_index, updating_variant['text'])
                        test.variants_ru.insert(inserting_variant_index, variant)
                    if user.lang == 'ru':
                        test.variants_uz.insert(inserting_variant_index, variant)
                        test.variants_ru.insert(inserting_variant_index, updating_variant['text'])

                    test.variants_uz.pop(updating_variant['index'])
                    test.variants_ru.pop(updating_variant['index'])

                    updated_variants_uz, updated_variants_ru = test.variants_uz, test.variants_ru

                    if exact_variant_uz == test.correct_answer_uz:
                        test_data.update(correct_answer_uz=updating_variant['text'], correct_answer_ru=variant) \
                            if user.lang == 'uz' else \
                            test_data.update(correct_answer_uz=variant, correct_answer_ru=updating_variant['text'])

                test_data.update(variants_uz=updated_variants_uz, variants_ru=updated_variants_ru)

        if data.get('correct_answer'):
            translated_correct_answer = await translator.translate(data['correct_answer'])

            index = test.variants_uz.index(test.correct_answer_uz)
            updating_insert = index + 1

            if user.lang == 'uz':
                test.variants_uz.insert(updating_insert, data['correct_answer'])
                test.variants_ru.insert(updating_insert, translated_correct_answer)
            if user.lang == 'ru':
                test.variants_uz.insert(updating_insert, translated_correct_answer)
                test.variants_ru.insert(updating_insert, data['correct_answer'])

            test.variants_uz.pop(index)
            test.variants_ru.pop(index)

            updated_variants_uz, updated_variants_ru = test.variants_uz, test.variants_ru

            test_data.update(variants_uz=updated_variants_uz, variants_ru=updated_variants_ru)

            test_data.update(correct_answer_uz=translated_correct_answer, correct_answer_ru=data['correct_answer']) \
                if language == 'uz' else \
                test_data.update(correct_answer_uz=data['correct_answer'], correct_answer_ru=translated_correct_answer)

        if file:
            if test.image:
                await File.remove(file_path=test.image)

            decoded_bytes = await to_thread(b64decode, file)

            image = UploadFile(BytesIO(decoded_bytes))

            file_path: str = await File(file=image).save(
                file_model_type=TEST, path=uploads_file_path, title=data['question']
            )

            test_data.update(image=file_path)

        test: Test = await self.repo.update(query=query, data=test_data)

        return self.response.success(data=test, status_code=200)

    async def delete(self, query):
        test: Test = await self.repo.retrieve(query=query)

        if test is None:
            return self.response.failure(
                data=dict(message=f'Test with this {query} query does not exists'), status_code=404
            )

        if test.is_testing:
            return self.response.failure(
                data=dict(message=f"Test with this {query} query is solving now"), status_code=400
            )

        section: Section = await Storage.section.retrieve(query=dict(id=test.section_id.id))

        if section.total_tests > 0:
            section.total_tests -= 1
            await section.update()

        if test.image:
            await File.remove(file_path=test.image)

        await self.repo.destroy(queryset=test)

        return self.response.success(data=dict(message=f"Test with this {query} has deleted"), status_code=204)

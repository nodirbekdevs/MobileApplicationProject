from fastapi import Request
from json import loads
from typing import List
from io import BytesIO
from xlsxwriter import Workbook
from datetime import datetime

from ..models import Test, Statistic, Instructor, tashkent_timezone
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, Filter, Populate, BOT
from ..static import comments
from ..utils import INSTRUCTOR, checking_solved_tests_format, translator


class StatisticController:
    def __init__(self):
        self.repo: CoreRepository = Storage.statistics
        self.response = SendResponse

    async def get_all(self, request: Request):
        params = request.query_params

        user = request.state.user

        filtering = dict()

        if user['role'] == INSTRUCTOR:
            filtering.update(instructor=user['id'])

        query: dict = Filter(query=filtering).filtering_with_params(params=params)

        statistics: List[Test] = await self.repo.list(query=query, populate=Populate.statistic)

        data = Pagination(params=params, datas=statistics, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_report(self, user):
        instructor: Instructor = await Storage.instructor.retrieve(query=dict(id=user['id']))

        statistics = await Storage.statistics.list(
            query=dict(instructor_id=user['id']),
            populate=Populate.statistic,
            order_by=['subject_id', 'section_id', 'student_id']
        )

        print(statistics)

        if statistics is None:
            return self.response.failure(status_code=404, data=dict(message="Statistics does not exist"))

        output = BytesIO()
        file_name = f"{datetime.now(tashkent_timezone).strftime('%Y-%m-%d %H:%M:%S')}_statistics_report.xlsx"
        header = ['№', "Instructor", "Talaba", 'Fan', "Bo'lim", 'Yechilgan testlar', 'Umimy testlar soni', "To'g'ri belgilanganlari", "Noto'g'ri belgilanganlari", "Foiz",
                  "Yechilgan vaqt"] if instructor.lang == 'uz' else ['№', "Инструктор", "Студент", 'Предмет', 'Секция', 'Решенные тесты', 'Общее количество тестов', 'Правильный счет', "Неправильный подсчет", "Процент",
                  "Время решения"]

        workbook = Workbook(output)
        bold = workbook.add_format({'bold': True})

        worksheet = workbook.add_worksheet(f"{instructor.name}")
        worksheet.write_row(0, 0, header, bold)

        row = 1

        for statistic in statistics:
            checked = loads(statistic.checked_tests)
            # statistic.checked_tests = loads(statistic.checked_tests)

            checked_tests = checking_solved_tests_format(checked, instructor.lang)

            worksheet.write(row, 0, row)
            worksheet.write(row, 1, statistic.instructor_id.name)
            worksheet.write_comment(row, 1, translator(comments['instructor']['uz'], comments['instructor']['ru'], instructor.lang))
            worksheet.write(row, 2, statistic.student_id.name)
            worksheet.write_comment(row, 2, translator(comments['student']['uz'], comments['student']['ru'], instructor.lang))
            worksheet.write(row, 3, statistic.subject_id.title_uz if instructor.lang == 'uz' else statistic.subject_id.title_ru)
            worksheet.write_comment(row, 3, translator(comments['subject']['uz'], comments['subject']['ru'], instructor.lang))
            worksheet.write(row, 4, statistic.section_id.title_uz if instructor.lang == 'uz' else statistic.section_id.title_ru)
            worksheet.write_comment(row, 4, translator(comments['section']['uz'], comments['section']['ru'], instructor.lang))
            worksheet.write(row, 5, checked_tests)
            worksheet.write_comment(row, 5, translator(comments['checked_tests']['uz'], comments['checked_tests']['ru'], instructor.lang), {'x_scale': 1.5, 'y_scale': 2.0})
            worksheet.write(row, 6, statistic.total_tests)
            worksheet.write_comment(row, 6, translator(comments['total_tests']['uz'], comments['total_tests']['ru'], instructor.lang))
            worksheet.write(row, 7, statistic.right_count)
            worksheet.write_comment(row, 7, translator(comments['right_count']['uz'], comments['right_count']['ru'], instructor.lang))
            worksheet.write(row, 8, statistic.wrong_count)
            worksheet.write_comment(row, 8, translator(comments['wrong_count']['uz'], comments['wrong_count']['ru'], instructor.lang))
            worksheet.write(row, 9, statistic.percentage)
            worksheet.write_comment(row, 9, translator(comments['percentage']['uz'], comments['percentage']['ru'], instructor.lang))
            worksheet.write(row, 10, statistic.solved_time)
            worksheet.write_comment(row, 10, translator(comments['solved_time']['uz'], comments['solved_time']['ru'], instructor.lang))

            row += 1

        worksheet.autofit()
        workbook.close()

        await BOT().send_document_to_bot(telegram_id=instructor.telegram_id, file=output.getvalue(), filename=file_name)

        return self.response.success(status_code=200, data=dict(message='SENT'))

    async def get_one(self, query: dict):
        statistic: Statistic = await self.repo.retrieve(query=query)

        statistic.checked_tests = loads(statistic.checked_tests)

        if statistic is None:
            return self.response.failure(
                data=dict(message=f'Statistic with this {query} query does not exists'), status_code=404
            )

        statistic = self.repo.schemas.retrieve(query=statistic)

        return self.response.success(data=statistic, status_code=200)

    async def create(self, user, data: dict):
        instructor = await Storage.instructor.retrieve(query=dict(id=data['instructor']))
        section = await Storage.section.retrieve(query=dict(id=data['section']))
        student = await Storage.instructor.retrieve(query=dict(id=user['id']))
        subject = await Storage.subject.retrieve(query=dict(id=data['subject']))

        data.update(instructor=instructor, section=section, student=student, subject=subject)

        statistic: Statistic = await self.repo.create(data=data)

        return self.response.success(data=statistic, status_code=201)

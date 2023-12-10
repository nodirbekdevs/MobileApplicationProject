from math import ceil
from ..services.schema_repository import SchemaRepository


class Pagination(object):
    def __init__(self, params, datas, schemas):
        self.params = params
        self.datas = datas
        self.schemas: SchemaRepository = schemas

    def paginate(self):
        page, page_size = int(self.params.get('page', 1)), int(self.params.get('page_size', 20))

        if not page or not page_size:
            return self.datas

        offset = (page - 1) * page_size
        end = offset + page_size

        data = self.datas[offset:end]

        total_pages = ceil(len(self.datas) / page_size)
        total_items = len(data)
        next_page = page + 1 if len(data) + offset != len(self.datas) else 'none'
        del self.datas
        prev_page = page - 1 if page != 1 else 'none'

        return dict(
            data=self.schemas.list(data=data),
            total_pages=total_pages,
            total_items=total_items,
            current_page=page,
            next_page=next_page,
            prev_page=prev_page
        )

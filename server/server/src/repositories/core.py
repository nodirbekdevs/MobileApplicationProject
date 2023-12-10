from datetime import datetime

from ..middlewares import logger
from ..models import tashkent_timezone


class CoreRepository(object):
    def __init__(self, model, scope: str, schemas=None):
        self.model = model
        self.scope = f"server.repositories.{scope}"
        self.schemas = schemas

    async def list(self, query: dict = None, populate: list = None, order_by: list = None):
        try:
            queryset = self.model.objects

            query = query.update(is_active=True) if query else dict(is_active=True)

            # if query:
            #     query.update(is_active=True)
            # else:
            #     query = dict(is_active=True)

            if populate:
                queryset = queryset.select_related(populate)

            if query:
                queryset = queryset.filter(**query)

            if order_by:
                queryset = queryset.order_by(order_by)

            return await queryset.all()
        except Exception as error:
            logger.error(f"{self.scope}.list: finished with error: {error}")
            raise

    async def retrieve(self, query: dict, populate=None):
        try:
            queryset = self.model.objects

            # query = query.update(is_active=True) if query else dict(is_active=True)
            print(query)
            if query:
                query.update(is_active=True)
            else:
                query = dict(is_active=True)
            print(query)
            queryset = queryset.filter(**query)

            if populate:
                queryset = queryset.select_related(populate)

            queryset = await queryset.get_or_none()

            if queryset is None:
                logger.warn(f"{self.scope}.retrieve failed to get_one")
                return None

            return queryset
        except Exception as error:
            logger.error(f"{self.scope}.retrieve: finished with error: {error}")
            raise

    async def create(self, data: dict, populate=None):
        try:
            queryset = await self.model.objects.create(**data)

            return self.schemas.retrieve(queryset)
        except Exception as error:
            logger.error(f"{self.scope}.create: finished with error: {error}")
            raise

    async def create_not_schemas(self, data: dict, populate=None):
        try:
            queryset = await self.model.objects.create(**data)

            return queryset
        except Exception as error:
            logger.error(f"{self.scope}.create: finished with error: {error}")
            raise

    async def update(self, query: dict, data: dict):
        try:
            queryset = await self.retrieve(query)

            for field, value in data.items():
                if value is not None:
                    setattr(queryset, field, value)

            queryset.updated_at = datetime.now(tashkent_timezone)

            queryset_data = await queryset.update()

            return self.schemas.retrieve(queryset_data)
        except Exception as error:
            logger.error(f"{self.scope}.update: finished with error: {error}")
            raise

    async def destroy(self, queryset):
        try:
            await queryset.delete()

            return True
        except Exception as error:
            logger.error(f"{self.scope}.destroy: finished with error: {error}")
            raise

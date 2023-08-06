import json
import logging
from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.db import transaction
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import path

from scrud_django import services
from scrud_django.models import Resource, ResourceType


def get_resource_type_for(slug):
    return get_list_or_404(ResourceType.objects.order_by("-revision"), slug=slug)[0]


class ResourceTypeRegistration:
    def __init__(
        self,
        resource_type_uri: str,
        revision: str,
        schema_resource: Resource = None,
        schema_func: str = None,
        schema_uri: str = None,
        context_resource: Resource = None,
        context_func: str = None,
        context_uri: str = None,
        slug: str = None,
    ):
        """
        Register resource type model.
        """
        search = ResourceType.objects.filter(type_uri=resource_type_uri)
        if search:
            self.resource_type = search[0]
        else:
            resource_type = ResourceType(
                type_uri=resource_type_uri,
                schema_uri=schema_uri,
                context_uri=context_uri,
                slug=slug,
                etag=uuid4().hex,
                modified_at=datetime.now(),
            )
            self.resource_type = resource_type

        if self.resource_type.revision != revision or settings.DEBUG:
            self.resource_type.revision = revision
            if schema_resource is None and schema_func:
                self.resource_type.schema = register_json_schema(
                    schema_func, self.resource_type.schema
                )
            if context_resource is None and context_func:
                self.resource_type.context = register_json_ld_context(
                    context_func, self.resource_type.context
                )
            self.resource_type.save()

        # Register with service catalog
        services.add_service(self.resource_type.type_uri, self.resource_type.slug)
        self.register_urls()

    def register_urls(self):
        """Register resource type url."""
        from scrud_django import views

        scrud_list = views.ResourceViewSet.as_view(
            {'get': 'list', 'head': 'list', 'post': 'create',},  # noqa: E231
            resource_type_name=self.resource_type.slug,
        )
        scrud_detail = views.ResourceViewSet.as_view(
            {
                'get': 'retrieve',
                'head': 'retrieve',
                'put': 'update',
                'delete': 'destroy',
            },
            resource_type_name=self.resource_type.slug,
        )
        self.urls = [
            path(
                f'{self.resource_type.slug}/',
                scrud_list,
                # name=f'{resource_type.slug}-list',
                name=self.resource_type.route_name_list(),
            ),
            path(
                f'{self.resource_type.slug}/<str:slug>/',
                scrud_detail,
                # name=f'{resource_type.slug}-detail',
                name=self.resource_type.route_name_detail(),
            ),
        ]


class ResourceRegistration:
    @staticmethod
    def register(content: str, register_type: str) -> Resource:
        """
        Register resource content for the given resource type name.

        Parameters
        ----------
        content : dict
        register_type : str

        Returns
        -------
        Resource

        """
        resource_type = get_resource_type_for(register_type)
        resource = Resource(content=content, resource_type=resource_type)
        resource = ResourceRegistration.register_instance(resource)
        return resource

    @staticmethod
    def register_instance(resource: Resource) -> Resource:
        """
        Register the resource for the given resource type.

        Parameters
        ----------
        resource : Resource
        resource_type : ResourceType

        Returns
        -------
        Resource

        """
        with transaction.atomic():
            resource.etag = uuid4().hex
            resource.modified_at = datetime.now()
            resource.resource_type.etag = resource.etag
            resource.resource_type.modified_at = resource.modified_at
            resource.save()
            resource.resource_type.save()
        return resource

    @staticmethod
    def update(content: str, register_type: str, slug: str) -> Resource:
        """
        Update resource content for the given resource type name and slug.

        Parameters
        ----------
        content : dict
        register_type : str
        slug : str

        Returns
        -------
        Resource

        """
        with transaction.atomic():
            resource_type = get_resource_type_for(register_type)

            # note: for now slug is used as ID
            resource = get_object_or_404(
                Resource, resource_type=resource_type, pk=int(slug)
            )

            resource.content = content
            resource.etag = uuid4().hex
            resource.modified_at = datetime.now()
            resource_type.etag = resource.etag
            resource_type.modified_at = resource.modified_at
            resource.save()
            resource_type.save()
        return resource

    @staticmethod
    def delete(register_type: str, slug: str):
        """
        Delete resource for the given resource type name and slug.

        Parameters
        ----------
        register_type : str
        slug : str

        """
        with transaction.atomic():
            resource_type = get_resource_type_for(register_type)

            # note: for now slug is used as ID
            resource = get_object_or_404(
                Resource, resource_type=resource_type, pk=int(slug)
            )
            resource.delete()
            resource_type.etag = uuid4().hex
            resource_type.modified_at = datetime.now()
            resource_type.save()


JSON_SCHEMA_REGISTRATION_ = None
JSON_SCHEMA_RESOURCE_TYPE_ = None
JSON_LD_RESOURCE_TYPE_ = None
JSON_LD_REGISTRATION_ = None


def register_json_schema_resource_type():
    global JSON_SCHEMA_RESOURCE_TYPE_
    global JSON_SCHEMA_REGISTRATION_
    if JSON_SCHEMA_RESOURCE_TYPE_ is None:
        JSON_SCHEMA_REGISTRATION_ = ResourceTypeRegistration(
            resource_type_uri="http://json-schema.org/draft-04/schema",
            revision="1",
            schema_uri="http://json-schema.org/draft-04/schema",
            slug="json-schema",
        )
        JSON_SCHEMA_RESOURCE_TYPE_ = JSON_SCHEMA_REGISTRATION_.resource_type
    return JSON_SCHEMA_RESOURCE_TYPE_


def register_json_ld_resource_type():
    global JSON_LD_RESOURCE_TYPE_
    global JSON_LD_REGISTRATION_
    if JSON_LD_RESOURCE_TYPE_ is None:
        JSON_LD_REGISTRATION_ = ResourceTypeRegistration(
            resource_type_uri="http://www.w3.org/ns/json-ld#context",
            revision="1",
            slug="json-ld",
        )
        JSON_LD_RESOURCE_TYPE_ = JSON_LD_REGISTRATION_.resource_type
    return JSON_LD_RESOURCE_TYPE_


def register_json_file(file_contents_func, previous_revision, resource_type):
    contents = file_contents_func()
    if type(contents) is str:
        contents = json.loads(contents)
    if previous_revision:
        resource = ResourceRegistration.update(
            contents, resource_type.slug, previous_revision.id
        )
    else:
        resource = ResourceRegistration.register(contents, resource_type.slug)
    return resource


def register_json_schema(schema_func, previous_revision):
    resource_type = register_json_schema_resource_type()
    return register_json_file(schema_func, previous_revision, resource_type)


def register_json_ld_context(context_func, previous_revision):
    resource_type = register_json_ld_resource_type()
    return register_json_file(context_func, previous_revision, resource_type)


def json_resource_type(
    resource_type_uri: str,
    revision: str,
    slug: str,
    schema_resource: Resource = None,
    schema_func=None,
    schema_uri: str = None,
    context_resource: Resource = None,
    context_func=None,
    context_uri: str = None,
):
    """Registration of a single json resource type. Callers **should** provide one and
    only one of `schema_resource, schema_path, schema_uri` as well as one and only  one
    of `context_resource, context_path, context_uri`.
    """
    try:
        resource_type_registration = ResourceTypeRegistration(
            resource_type_uri,
            revision,
            slug=slug,
            schema_resource=schema_resource,
            schema_func=schema_func,
            schema_uri=schema_uri,
            context_resource=context_resource,
            context_func=context_func,
            context_uri=context_uri,
        )
        return resource_type_registration.urls
    except (OperationalError, ProgrammingError):
        logging.warning(
            "Failed to register resource type due to OperationalError. "
            "This is expected for migrations."
        )
    return []


def resource_types(*args):
    """Convenience function to make the configuration of resource type registrations
    more readable.
    """
    ret = []
    for urls in args:
        ret.extend(urls)
    return ret

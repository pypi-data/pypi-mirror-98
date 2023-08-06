from typing import Type

from flask_restx import Model, Namespace, Resource
from mongoengine import Document

from businessman.business_logic.utils import get_crud_BusinessLogic


def crud_controller_factory(model: Type[Document],
                            schema_class: Model,
                            **kwargs) -> Namespace:
	"""
	:param model:
	:param schema_class: restx model as output schema
	:return: restx namespace

	kwargs optional params: ["name","CRUD_service_class","route"]
	"""
	name = kwargs.get("name") or model.__name__
	route = kwargs.get("route") or f"{name.lower()}"
	ns = Namespace(route, description=f'{name} related operations')

	schema_class = ns.model(name, schema_class)

	CRUD_service = get_crud_BusinessLogic(CRUD_base_cls=kwargs.get("CRUD_service_class"), model=model)

	@ns.route("/")
	class ObjectList(Resource):
		"""
			None Parametric API class
		"""
		CRUD_Service = CRUD_service
		schema = schema_class

		@ns.doc(f"object_list {name}")
		# @ns.marshal_list_with(schema)
		def get(self):
			"""Object List"""
			return self.CRUD_Service.get_all()

		@ns.doc('create_object')
		@ns.expect(schema)
		# @ns.marshal_with(schema, code=201)
		def post(self):
			"""Create Object"""
			return self.CRUD_Service.create(ns.payload), 201

	@ns.route('/<int:pk>')
	@ns.param('pk', 'The Object identifier')
	@ns.response(404, 'Object not found')
	class ObjectByParam(Resource):
		CRUD_Service = CRUD_service
		schema = schema_class

		@ns.doc('get_object')
		@ns.marshal_with(schema)
		def get(self, pk):
			"""Object Detail"""
			obj = self.CRUD_Service.get_by_id(pk)
			if obj:
				return obj
			else:
				ns.abort(404)

		@ns.doc('update_object')
		@ns.expect(schema)
		@ns.marshal_with(schema, code=201)
		def put(self, pk):
			"""Update Object"""
			pass

		@ns.doc('delete_object')
		def delete(self, pk):
			"""Delete Object"""
			pass

	return ns

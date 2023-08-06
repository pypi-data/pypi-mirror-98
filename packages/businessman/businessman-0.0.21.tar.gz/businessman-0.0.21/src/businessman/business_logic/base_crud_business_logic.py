import json
from typing import Any, Dict, List, Union

from mongoengine import Document

from .base_business_logic import BaseBusinessLogic


class BaseCRUDBusinessLogic(BaseBusinessLogic):
	model: Document = None

	@classmethod
	def get_form(cls):
		# TODO get form from model
		form = cls.form
		if not form:
			pass
		return form

	@classmethod
	def get_all(cls) -> List[model]:
		"""
		:return: all object of model
		"""
		return list(map(lambda x: json.loads(x.to_json()), cls.model.objects))

	@classmethod
	def get_all_pagination(cls, after: Union[str, int] = None, first: int = 0, ) -> Dict[str, Any]:
		"""
		:param first: count of object after $after
		:param after: first object as courser
		:return: List of [model] object paginated

		"""
		# TODO from $after object count of $first
		# TODO It must Contain filter for object
		# TODO add [hasNextPage], [hasPreviousPage], [Count]
		# TODO add filtering for object
		res = {
			"hasNextPage": True,
			"hasPreviousPage": True,
			"data": []
		}
		return res

	@classmethod
	def get_by_id(cls, object_id: Union[str, int]) -> model:
		pass

	@classmethod
	def create(cls, payload: Dict) -> model:
		# TODO check with form
		# TODO create new object

		# model_form = cls.get_form()
		# form = model_form(payload)
		# if form.validate():
		# 	pass
		pass

	@classmethod
	def update(cls) -> model:
		pass

	@classmethod
	def delete(cls, object_id: Union[str, int]) -> None:
		pass

from .write import Write
from .exceptions import InputError
from collections import OrderedDict


class Create(Write):
    def __init__(self, request, authentication, models):
        super().__init__(request, authentication, models)

    def handle(self):
        model = self._models.empty_model()
        input_data = self.json_body()
        input_errors = {
            **self._extra_column_errors(input_data),
            **self._find_input_errors(model, input_data),
        }
        if input_errors:
            raise InputError(input_errors)
        model.save(input_data)

        return self.success(self._model_as_json(model))

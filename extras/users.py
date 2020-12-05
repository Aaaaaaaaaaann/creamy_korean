from django.core.exceptions import ObjectDoesNotExist


class ProfileHandler:

    @staticmethod
    def existing(model, ids):
        output = []
        for i in ids:
            try:
                model.objects.get(pk=i)
            except ObjectDoesNotExist:
                continue
            else:
                output.append(i)
        return output
    

    @staticmethod
    def make_action(context, field, model):
        action = context['action']
        values = context['values']

        if not isinstance(values, list):
            values = [values]

        if action == 'add':
            values = ProfileHandler.existing(model, set(values))
            if field is None:
                field = values
            else:
                for value in values:
                    if value not in field:
                        field.append(value)
                
        elif action == 'remove':
            if field is None:
                return
            for value in values:
                try:
                    field.remove(value)
                except KeyError:
                    continue

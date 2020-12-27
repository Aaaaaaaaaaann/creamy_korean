from django.core.exceptions import ObjectDoesNotExist


class ProfileHandler:
    """
    A class contain methods for checking and updating
    entries values of UserProfile model.
    """

    @staticmethod
    def existing(model, ids):
        """
        Get a sequence of IDs and return those of them
        that exist in the database.
        """
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
    def make_action(data):
        """
        Change values in database field array
        based on request context.
        """
        action = data['action']
        values = data['values']

        if not isinstance(values, list):
            values = [values]

        if action == 'add':
            values = ProfileHandler.existing(data['model'], set(values))
            if (field := data['field']) is None:
                field = values
            else:
                for value in values:
                    if value not in field:
                        field.append(value)
                
        elif action == 'remove':
            if (field := data['field']) is None:
                return
            for value in values:
                try:
                    field.remove(value)
                except KeyError:
                    continue
    
    @staticmethod
    def get_values(field, model):
        """Return names of related field values as strings."""
        if not field:
            return
        output = []
        for value in field:
            output.append({
                'id': value,
                'name': model.objects.get(pk=value).name
            })
        return output

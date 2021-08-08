class ModelsSorterABC:
    def __init__(self, model_class, queryset):
        self.model_class = model_class
        self.queryset = queryset

    def get_attrs_instances_list(self):
        raise NotImplementedError

    def get_attr_instance_name(self, attr_instance):
        raise NotImplementedError

    def get_attr_instance_class_postfix(self, attr_instance):
        raise NotImplementedError

    def get_attr_instance_id(self, attr_instance):
        raise NotImplementedError

    def get_attr_instance_sorted_list(self, attr_instance):
        raise NotImplementedError

    def execute(self, parent_id=''):
        dicts = []
        for attr_instance in self.get_attrs_instances_list():
            attr_instance_dict = {
                'name': self.get_attr_instance_name(attr_instance),
                'class_postfix': self.get_attr_instance_class_postfix(attr_instance),
                'id': self.get_attr_instance_id(attr_instance),
                'list': self.get_attr_instance_sorted_list(attr_instance)
            }
            if parent_id != '':
                attr_instance_dict['id'] += f'_in_{parent_id}'
            dicts.append(attr_instance_dict)
        return dicts


def get_dates_with_notes(notes):
    dates = set()
    for note in notes:
        dates.add(note.date)
    return sorted(list(dates), reverse=True)


class ServiceNoteDateSorter(ModelsSorterABC):
    def get_attrs_instances_list(self):
        return get_dates_with_notes(self.queryset)

    def get_attr_instance_name(self, attr_instance):
        return attr_instance

    def get_attr_instance_class_postfix(self, attr_instance):
        return 'primary'

    def get_attr_instance_id(self, attr_instance):
        return f'id_date_{attr_instance}'

    def get_attr_instance_sorted_list(self, attr_instance):
        return self.queryset.filter(date=attr_instance).extra(order_by=['date'])


class ServiceNoteStatusSorter(ModelsSorterABC):
    def get_attrs_instances_list(self):
        return range(len(self.model_class.STATUS_CHOICES))

    def get_attr_instance_name(self, attr_instance):
        return self.model_class.STATUS_CHOICES[attr_instance][1]

    def get_attr_instance_class_postfix(self, attr_instance):
        return self.model_class.STATUS_CSS_CLASSES[attr_instance][1]

    def get_attr_instance_id(self, attr_instance):
        return f'id_status_{attr_instance}'

    def get_attr_instance_sorted_list(self, attr_instance):
        return self.queryset.filter(
            status=self.model_class.STATUS_CSS_CLASSES[attr_instance][0]
        ).extra(order_by=['date', 'time_start'])

import json
from enum import Enum

from .Elements import Elements
from .Exceptions import BuildFilterError
from .Filter import FilterFactory, _FDUFilter


class FiltersKeys(Enum):
    name_key = "name"
    properties_key = "properties"
    dimension_key = "dimensions"
    partitions_key = "partitions"
    attrName_key = 'attributeName'


class Filters(Elements):
    """Class allowing to get access to the list of defined filters
    """

    def __init__(self):
        """
        Initialize and build our list of filters
        """
        super().__init__()
        # Keeps the filters as dictionary (useful when update DB)
        self._filters_as_dic = []

    def _update(self):
        """Update the list of filter to make sure it's consistent with our database.
        """
        filters_description = self.request.get_in_python(self.url_manager.filter_list_url())
        self._elements = {}
        self._filters_as_dic = []
        for filter_description in filters_description[FiltersKeys.dimension_key.value]:
            filt = FilterFactory.build_filter(filter_dic = filter_description)
            if filt is not None:
                self._elements[filt.name] = filt
                self._filters_as_dic.append(filter_description)
            else:
                print('ERROR in filter argument')

    def get_with_id(self, filter_id):
        """Look for a particular group in the list using its id

        :param filter_id: id of the group to look for
        :return: the required group or None if nothing found
        """
        self._update()
        filter_id = filter_id.strip()
        for key, filter_description in self._elements.items():
            if filter_description.id == filter_id:
                return filter_description
        return None

    def all_fdu(self):
        """
        :return: the list of FDU filters' values
        """

        self._update()
        fdu_filters = {}
        for key, filt in self._elements.items():
            if isinstance(filt, _FDUFilter):
                fdu_filters[key] = filt
        return fdu_filters.values()

    @staticmethod
    def _label_already_used(filtering_values, label):
        """Check if a given label is already used
        In the list of filtering values, a label can only be used once

        :return: True if label found. False otherwise
        """
        for element in filtering_values:
            if element[FiltersKeys.name_key.value] == label:
                return True
        return False

    @staticmethod
    def _build_partition_1_attr(field, filtering_values):
        """Builds the structure for the list of filtering_values ('partitions') for 1 attributes

        :param field: Name of the field concerned
        :param filtering_values: list of values where to do the filtering
        :return: The list of filtering values (partitions) created
        """
        partitions = []
        for filtering_val in filtering_values:
            if Filters._label_already_used(partitions, filtering_val):
                print('[ERR FILTERING_VALUES] label', filtering_val, 'already in list so not added')
                continue
            partitions.append({FiltersKeys.name_key.value: filtering_val,
                               FiltersKeys.properties_key.value: {field: filtering_val}})
        return partitions

    @staticmethod
    def _build_partitions_attributes(fields, filtering_values, field_for_label=None):
        """Builds the structure for the list of filtering_values ('partitions') for >1 attributes

        :param fields: Name of the fields concerned
        :param filtering_values: list of values on which do the filtering
        :param field_for_label: If FDU is on several fields, chose one for label initialization.
        :return: The list of filtering values (partitions) created
        """
        partitions = []
        for filtering_vals in filtering_values:
            if len(filtering_vals) != len(fields):
                return None
            if field_for_label is not None and field_for_label not in fields:
                print('Field_for_label "{}" not in fields so ignored'.format(field_for_label))
                field_for_label = None
            element = {FiltersKeys.name_key.value: '', FiltersKeys.properties_key.value: {}}
            for field, filtering_val in zip(fields, filtering_vals):
                if field_for_label is None and not element[FiltersKeys.name_key.value]:
                    element[FiltersKeys.name_key.value] = filtering_val
                elif field_for_label is not None and field == field_for_label:
                    element[FiltersKeys.name_key.value] = filtering_val
                element[FiltersKeys.properties_key.value][field] = filtering_val
            if Filters._label_already_used(partitions, element[FiltersKeys.name_key.value]):
                print('[ERROR FILTERING_VALUES] label', element[FiltersKeys.name_key.value],
                      'already in list')
                continue
            partitions.append(element)
        return partitions

    def _build_list_filtering_values(self, fields, filtering_values, field_for_label=None):
        """Builds the structure for the list of filtering_values (partitions) in a FDU

        :param fields: Fields concerned by the filter.
        :param filtering_values: Filtering values corresponding to the fields for the fdu.
        :param field_for_label: If FDU is on several fields, chose one for label initialization.
        :return: the structure or None if there's a problem in creation
        """
        if len(fields) > 1:
            return self._build_partitions_attributes(fields, filtering_values, field_for_label)
        elif len(fields) == 1:
            return self._build_partition_1_attr(fields[0], filtering_values)
        return None

    def add_FDU_filter(self, name, fields, filtering_values, properties=None, field_for_label=None):
        """Add a new FDU filter to our database

        :param name: Filter name
        :param fields: List of fields concerned by the filter
        :param filtering_values: List of values for the field(s) concerned by the filter
        :param properties: # TODO Determine this parameter
        :param field_for_label: If FDU is on several fields, chose one for label initialization.
        """
        # TODO check if filtering values are in selected field ?
        try:
            list_filtering_values = self._build_list_filtering_values(fields,
                                                                      filtering_values,
                                                                      field_for_label)
            if list_filtering_values is None:
                raise BuildFilterError('[ERROR FDU] Error while creating list of filtering values')
        except BuildFilterError as e:
            print(e.args)
            return
        fdu_filter = FilterFactory.build_filter(name = name, attributes = fields,
                                                filtering_values = list_filtering_values,
                                                properties = properties,
                                                filter_type = "fdu")
        self._add(fdu_filter)

    def add_SQL_filter(self, name, where_clause):
        """Add a new SQL Filter to our database

        :param name: Filter name
        :param where_clause: Values wanted for the filter (eg : 'type = Herbes')
        """
        # Create an instance of the new filter to add
        sql_filter = FilterFactory.build_filter(name = name, where_clause = where_clause,
                                                filter_type = "sql")
        # add it to our list
        self._add(sql_filter)

    def replace_fdu_values(self, filter_name, filtering_values, field_for_label=None):
        """Updates a given FDU. Replacing its value
        :param filter_name:
        :param filtering_values: List of values for the field(s) concerned by the filter
        :param field_for_label: If FDU is on several fields, chose one for label initialization.
        """
        self._update()
        if not self._filter_exist_already(filter_name):
            print("Filter not in list. Can't update it.")
            return
        fdu_filter = self.get(filter_name)
        self._apply_update_on_fdu_fv(fdu_filter, filtering_values, field_for_label)

    def add_values_to_fdu(self, filter_name, filtering_values, field_for_label=None):
        """Adds new filtering values to a fdu.
        :param filter_name:
        :param filtering_values: List of values for the field(s) concerned by the filter
        :param field_for_label: If FDU is on several fields, chose one for label initialization.
        """
        self._update()
        if not self._filter_exist_already(filter_name):
            print("Filter not in list. Can't update it.")
            return
        fdu = self.get(filter_name)
        all_values = list(set(fdu.get_labels() + filtering_values))
        self._apply_update_on_fdu_fv(fdu, all_values, field_for_label)

    def remove_values_from_fdu(self, filter_name, removed_fv, field_for_label=None):
        """Removes filtering values from a fdu.
        :param filter_name:
        :param removed_fv: List of values for the field(s) concerned by the filter
        :param field_for_label: If FDU is on several fields, chose one for label initialization.
        """
        self._update()
        if not self._filter_exist_already(filter_name):
            print("Filter not in list. Can't update it.")
            return
        fdu = self.get(filter_name)
        # Removes f_v from fdu that are not in the list to remove
        all_values = list(set(fdu.get_labels()) - set(removed_fv))
        self._apply_update_on_fdu_fv(fdu, all_values, field_for_label)

    def _apply_update_on_fdu_fv(self, fdu, filtering_values, field_for_label=None):
        """Applies a given change on filtering_values for fdu
        :param fdu:
        :param filtering_values: new filtering_values
        :param field_for_label:
        """
        try:
            list_filtering_values = self._build_list_filtering_values(fdu.get_fields(),
                                                                      filtering_values,
                                                                      field_for_label)
            if list_filtering_values is None:
                raise BuildFilterError('[ERROR FDU] Error while creating list of filtering values')
        except BuildFilterError as e:
            print(e.args)
            return
        new_fdu = FilterFactory.build_filter(name = fdu.get_name(), attributes = fdu.get_fields(),
                                             filtering_values = list_filtering_values,
                                             properties = fdu.properties,
                                             filter_type = "fdu")

        self._update_fdu_on_filter_dict(new_fdu)
        self._apply_changes()
        print('Filter "{}" successfully updated !'.format(fdu.get_name()))

    def update_sql_filter_value(self, filter_name, where_clause):
        """Replace a given sql filter's where clause
        :param filter_name:
        :param where_clause: new value to set
        """
        self._update()
        if not self._filter_exist_already(filter_name):
            print("Filter not in list. Can't update it.")
            return
        self._update_fsql_on_filter_dict(filter_name, where_clause)
        self._apply_changes()
        print('Filter "{}" successfully updated !'.format(filter_name))

    def create_filter(self):  # TODO
        """
        :return: a new Filter instance

        ..warning not implemented
        """
        pass

    def remove_filter(self, filter_name):
        """If possible, removes a specified filter from Orion
        :param filter_name: Identifies filter to remove
        """
        if not filter_name:
            return
        self._update()
        if not self._filter_exist_already(filter_name):
            print("Filter not in list. Doesn't need to do anything.")
            return
        removed_filter = self.get(filter_name)
        if removed_filter is None:
            print("Filter not found. Doesn't need to do anything.")
            return
        if removed_filter.properties and removed_filter.properties['deletionForbidden']:
            print("Deletion forbidden on this filter")
            return

        # Remove it from our list and applies it on the server.
        self._rmv_from_filter_dict(removed_filter)
        self._apply_changes()
        print('Filter "{}" successfully removed !'.format(filter_name))

    def _add(self, new_filter):
        """Add a new filter to Orion.

        :param new_filter: The new filter to add.
        """
        if new_filter is None:  # if there was a problem in creation
            return
        self._update()
        # If the filter is already in the db, don't add it
        if self._filter_exist_already(new_filter.name):
            print('Filter "{}" already exist in db'.format(new_filter.name))
            return
        self._add_to_filter_dict(new_filter)
        # get the formatted list for request and add this in the DB
        self._apply_changes()
        print('Filter "{}" successfully added !'.format(new_filter.name))

    def add_list(self, new_filters):
        """Add a list of filters to the database.

        :param new_filters: list of all filters and updates (add/delete/edit)
        """
        self._update()
        something_to_add = False  # Avoid to make a request if there's nothing to add
        for filt in new_filters:
            if not self._filter_exist_already(filt.name):
                something_to_add = True
                self._add_to_filter_dict(filt)
        if something_to_add:
            self._apply_changes()

    def _add_to_filter_dict(self, filt):
        """Add filter to the dictionary (useful for list-modification requests)
        """
        # TODO improve it !!! (work is based on FDUfilter's attributes name...)
        self._filters_as_dic.append(filt.__dict__)

    def _rmv_from_filter_dict(self, removed_filter):
        """ Removes removed_filter from our list.
        :param removed_filter:
        """
        self._filters_as_dic = list(
            filter(lambda x: x['name'] != removed_filter.name, self._filters_as_dic)
        )

    def _update_fsql_on_filter_dict(self, filter_name, where_clause):
        """Updates a given sql filter on our list.
        Note that the method place the updated filter at the end of _filters_as_dic.
        :param filter_name:
        :param where_clause:
        """
        tmp_lst = [f for f in self._filters_as_dic if f['name'] != filter_name]
        sql_filters = [f for f in self._filters_as_dic if f['name'] == filter_name]
        sql_filters[0]['whereClause'] = where_clause
        tmp_lst.append(sql_filters[0])
        self._filters_as_dic = tmp_lst

    def _update_fdu_on_filter_dict(self, fdu):
        """Updates a given FDU filter on our list
        :param fdu: _FDUFilter type. The filter we want to update.
        """
        tmp_lst = [f for f in self._filters_as_dic if
                   f[FiltersKeys.name_key.value] != fdu.get_name()]
        fdus = [f for f in self._filters_as_dic if
                f[FiltersKeys.name_key.value] == fdu.get_name()]
        fdus[0][FiltersKeys.partitions_key.value] = fdu.partitions
        fdus[0][FiltersKeys.attrName_key.value] = fdu.get_fields()
        tmp_lst.append(fdus[0])
        self._filters_as_dic = tmp_lst

    def _filters_formatted(self):
        """For list-modification request.

        :return: a json formatted string with the same format as required by Orion
        """
        return json.dumps({'dimensions': self._filters_as_dic})

    def _apply_changes(self):
        """For all changes, a request is sent with the full filter list to the configure uri.
        """
        self.request.post(self.url_manager.filter_config_url(),
                          {'value': self._filters_formatted()})

    def _filter_exist_already(self, name, filters=None):
        """Check if a given filter name is already in database

        :rtype: bool
        :param name: the name of the new filter to check
        :param filters: list of filters (up to date with db)
        :return: a boolean to say if filter already added or not
        """
        if filters is None:
            filters = self._elements
        return name in filters

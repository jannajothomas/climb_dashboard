import numpy
from flask import session


def get_unique_list_from_list_column(this_list, column):
    transposed_list = numpy.transpose(this_list)
    unique_list = numpy.unique(transposed_list[column])
    return unique_list


def update_args(new_form_values, my_dict):
    for current_item in my_dict:
        for new_item in new_form_values:
            if current_item == new_item:
                my_dict[current_item] = new_form_values[new_item]
    return my_dict


def toggle_view_buttons(key):
    if key == 'view_completed':
        session['view_remaining'] = 'False'
        session['view_all'] = 'False'
    elif key == 'view_remaining':
        session['view_completed'] = 'False'
        session['view_all'] = 'False'
    elif key == 'view_all':
        session['view_remaining'] = 'False'
        session['view_completed'] = 'False'


def get_converted_name(name_selected):
    iter1 = name_selected.replace("\'", "")
    iter2 = iter1.replace("(", "")
    iter3 = iter2.replace(")", "")
    iter4 = iter3.replace(" ", "")
    name = iter4.split(",")[0]
    id_num = iter4.split(",")[1]
    return name, id_num

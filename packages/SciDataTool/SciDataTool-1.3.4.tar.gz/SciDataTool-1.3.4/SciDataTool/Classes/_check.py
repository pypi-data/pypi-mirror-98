# -*- coding: utf-8 -*-

from numpy import array, empty, int32, squeeze, expand_dims


def set_array(obj, prop, value):
    """Set an array that can be None or a list
    Parameters
    ----------
    obj : ?
        Object to set
    prop : str
        Name of the property to set
    value : ?
        Value to set
    Returns
    -------
    None
    """
    if value is None:  # Default value
        value = empty(0)
    elif isinstance(value, list):
        value = array(value)
    setattr(obj, prop, value)


def check_init_dict(init_dict, key_list):
    """Check if init_dict is correct to initialize the Object (all the keys of init_dict are in key_list)
    Parameters
    ----------
    init_dict : dict
        The dictionary to check
    key_list : list
        List of the expected key (str)
    Returns
    -------
    None
    Raises
    ------
    NotADictError
        init_dict is not a dictionary
    MissingInitDictKeyError
        A key is missing in init_dict
    """
    if not isinstance(init_dict, dict):
        raise NotADictError("Init by dict : init_dict must be a dict")
    msg = "Second argument is the list of variable needed in init_dict"
    assert isinstance(key_list, list), msg
    # Check that every key of init_dict is expected for this object
    key_list.append("__class__")  # Not a property, added for load
    for key in list(init_dict.keys()):
        if key not in key_list:
            raise UnknowInitDictKeyError("Init by dict : " + key + " is not a property")


def check_var(var_name, value, expect_type, Vmin=None, Vmax=None):
    """Check if var_name can be set with value
    Parameters
    ----------
    var_name : str
        The name of the property to set
    value : ?
        The value to check
    expected_type : str
        The name of the expected type for value
    Vmin : float
        Value must be >Vmin (None if the property has no Vmin) (Default value = None)
    Vmax : float
        Value must be <Vmax (None if the property has no Vmax) (Default value = None)
    Returns
    -------
    None
    Raises
    ------
    CheckError
        The value is incorrect for var_name
    """
    if value is not None:
        type_value = type(value).__name__
        if type_value == "float64":
            type_value = "float"
        # Check if value has the good type
        check_type(var_name, value, expect_type, type_value)
        # Check if value is in the good range (if needed)
        if Vmin is not None:
            check_min(var_name, value, type_value, Vmin)
        if Vmax is not None:
            check_max(var_name, value, type_value, Vmax)


def check_type(var_name, value, expect_type, type_value):
    """Check if value has the expected type for var_name
    Parameters
    ----------
    var_name : str
        The name of the property to set
    value : ?
        The value to check
    expected_type : str
        The name of the expected type for value (str)
    type_value :
        The name of the actual type of the variable
    expect_type :
    Returns
    -------
    Raises
    ------
    CheckTypeError
        Value has a wrong type for var_nam
    """
    if expect_type == "float":  # float variable can take int value
        if not (
            (isinstance(value, int32) and not isinstance(value, bool))
            or (isinstance(value, int) and not isinstance(value, bool))
            or isinstance(value, float)
        ):
            raise CheckTypeError(
                "For " + var_name + " : Double expected, " + type_value + " given"
            )
    elif expect_type == "complex":
        # complex variable can take float or int value
        if not (
            (isinstance(value, int) and not isinstance(value, bool))
            or isinstance(value, float)
            or isinstance(value, complex)
        ):
            raise CheckTypeError(
                "For " + var_name + " : Complex expected, " + type_value + " given"
            )
    elif expect_type == "str":
        if not isinstance(value, str):
            raise CheckTypeError(
                "For " + var_name + " : String expected, " + type_value + " given"
            )
    elif expect_type == "list":
        if not isinstance(value, list):
            raise CheckTypeError(
                "For " + var_name + " : list expected, " + type_value + " given"
            )
    elif expect_type == "int" and type_value == "float":
        if value % 1 != 0:  # If not an Integer
            raise CheckTypeError(
                "For " + var_name + " : Integer expected, " + type_value + " given"
            )
    elif expect_type == "int" and type_value == "int32":
        if value % 1 != 0:  # If not an Integer
            raise CheckTypeError(
                "For " + var_name + " : Integer expected, " + type_value + " given"
            )
    elif expect_type[0] == "[" and expect_type[-1] == "]":  # List of type
        if not isinstance(value, list):
            raise CheckTypeError(
                "For " + var_name + " : List expected, " + type_value + " given"
            )
        # Check type of value element
        expect_type = expect_type[1:-1]
        for element in value:
            type_value = type(element).__name__
            # Check if it's the expected type
            if not type_value == expect_type:
                # Check if object inherit from the expected type
                mother = element.__class__.__bases__  # List of inherited class
                find = False  # Store the result of the research
                while mother != ():  # Every class inherit from FrozenClass
                    if mother[0].__name__ == expect_type:
                        find = True
                        break
                    else:
                        mother = mother[0].__bases__
                if not find:  # Not the good type
                    raise CheckTypeError(
                        "For "
                        + var_name
                        + " : "
                        + expect_type
                        + " expected, "
                        + type_value
                        + " given"
                    )
    elif expect_type[0] == "{" and expect_type[-1] == "}":  # Dict of type
        if not isinstance(value, dict):
            raise CheckTypeError(
                "For " + var_name + " : Dict expected, " + type_value + " given"
            )
        # Check type of value element
        expect_type = expect_type[1:-1]
        for key, element in value.items():
            type_value = type(element).__name__
            # Check if it's the expected type
            if not type_value == expect_type:
                # Check if object inherit from the expected type
                mother = element.__class__.__bases__  # List of inherited class
                find = False  # Store the result of the research
                while mother != ():  # Every class inherit from FrozenClass
                    if mother[0].__name__ == expect_type:
                        find = True
                        break
                    else:
                        mother = mother[0].__bases__
                if not find:  # Not the good type
                    raise CheckTypeError(
                        "For "
                        + var_name
                        + " : "
                        + expect_type
                        + " expected, "
                        + type_value
                        + " given"
                    )
    else:
        if not type_value == expect_type:  # Check if it's the expected type
            if expect_type in ["int", "bool", "str"]:
                # We don't check inheritance for python type
                raise CheckTypeError(
                    "For "
                    + var_name
                    + " : "
                    + expect_type
                    + " expected, "
                    + type_value
                    + " given"
                )
            else:
                # Check if object inherit from the expected type
                mother = value.__class__.__bases__  # List of inherited class
                find = False  # Store the result of the research
                while mother != ():  # Every class inherit from FrozenClass
                    if mother[0].__name__ == expect_type:
                        find = True
                        break
                    else:
                        mother = mother[0].__bases__
                if not find:  # Not the good type
                    raise CheckTypeError(
                        "For "
                        + var_name
                        + " : "
                        + expect_type
                        + " expected, "
                        + type_value
                        + " given"
                    )


def check_min(var_name, value, type_value, Vmin):
    """Check if value is greater than the min of var_name
    Parameters
    ----------
    var_name : str
        The name of the property to set
    value : ?
        The value to check (int, float or ndarray)
    type_value : str
        The name of the actual type of the variable
    Vmin : float
        Value must be >Vmin
    Returns
    -------
    None
    Raises
    ------
    CheckMinError
        value is too small for var_nam
    """
    # Work only for number and matrix
    msg = "Check : You can't specify the min of variable of type " + type_value
    assert type_value in ["ndarray", "int", "long", "float", "int32"], msg
    # For number
    if (isinstance(value, int) or isinstance(value, float)) and value < Vmin:
        raise CheckMinError(
            var_name + " must be >= " + str(Vmin) + ", " + str(value) + " given"
        )
    # For non empty matrix
    if type_value == "ndarray" and value.size > 0 and value.min() < Vmin:
        raise CheckMinError(
            var_name
            + " must have its elements >= "
            + str(Vmin)
            + ", "
            + str(value)
            + " given"
        )


def check_max(var_name, value, type_value, Vmax):
    """Check if value is less than the max of var_name
    Parameters
    ----------
    var_name : str
        The name of the property to set
    value : ?
        The value to check (int, float or ndarray)
    type_value : str
        The name of the actual type of the variable
    Vmax : float
        Value must be <Vmax
    Returns
    -------
    None
    Raises
    ------
    CheckMaxError
        value is too large for var_nam
    """
    # Work only for number and matrix
    msg = "Check : You can't specify the max of variable of type " + type_value
    assert type_value in ["ndarray", "int", "long", "float", "int32"], msg
    # For number
    if (isinstance(value, int) or isinstance(value, float)) and value > Vmax:
        raise CheckMaxError(
            var_name + " must be <= " + str(Vmax) + ", " + str(value) + " given"
        )
    # For non empty matrix
    if type_value == "ndarray" and value.size > 0 and value.max() > Vmax:
        raise CheckMaxError(
            var_name
            + " must have its elements <= "
            + str(Vmax)
            + ", "
            + str(value)
            + " given"
        )


def raise_(ex):
    """Function to raise an exeption for the method import lambda"""
    raise ex


def check_dimensions(values, axes):
    """Check if field and axes have matching dimensions
    Parameters
    ----------
    values : ndarray
        values array
    axes : [Data]
        list of Data objects
    Returns
    -------
    None
    Raises
    ------
    CheckDimError
        Dimensions of field and axes do not match
    """
    if isinstance(values, list):
        values = array(values)
    else:
        values = values
    values_shape = values.shape
    axes_shape = []
    for axis in axes:
        if hasattr(axis, "values"):
            axes_shape.append(axis.values.size)
        else:
            try:
                axes_shape.append(int(axis.number))
            except:
                axes_shape.append(round((axis.final - axis.initial) / axis.step))

    if values_shape != tuple(axes_shape):
        for i, s in enumerate(axes_shape):
            if s == 1:
                values = expand_dims(values, axis=i)
        if values.shape != tuple(axes_shape):
            raise CheckDimError(
                "Dimensions of field ("
                + str(values_shape)
                + ") and axes ("
                + str(tuple(axes_shape))
                + ") do not match"
            )
    return values


class CheckDimError(Exception):
    """ """

    pass


class CheckError(Exception):
    """ """

    pass


class CheckMinError(CheckError):
    """ """

    pass


class CheckMaxError(CheckError):
    """ """

    pass


class CheckTypeError(CheckError):
    """ """

    pass


class InitUnKnowClassError(CheckError):
    """ """

    pass


class UnknowInitDictKeyError(CheckError):
    """ """

    pass


class NotADictError(CheckError):
    """ """

    pass

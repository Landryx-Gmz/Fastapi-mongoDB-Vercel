### Type Hints ###

my_string_variable = "my String variable"
print(my_string_variable)
print(type(my_string_variable))

my_string_variable = 4
print(my_string_variable)
print(type(my_string_variable))

my_typed_variable : str = "My taped String variable"
print(my_typed_variable)
print(type(my_typed_variable))

my_typed_variable = 5
print(my_typed_variable)
print(type(my_typed_variable))


# Con : str cuando llamamos a los metodos disponible con . nos aparece las del tipo que hemos definido
# si utilizamo : int seran otros metodos del timpo numerico lo que nos mostrara el ide 
def get_full_name(first_name: str, second_name:str):
    full_name= first_name.title() + " " + second_name.title()
    return full_name
print(get_full_name("andy","gomez"))
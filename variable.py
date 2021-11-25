import re
from typing import List
from dataclasses import dataclass
from helper import verboseprint

TYPEDEFS = ["int", "char", "long"]
VARIABLE_SEARCH_REGEX = re.compile(
    fr'(({"|".join([ fr"(?:{vartype})" for vartype in TYPEDEFS])})(?:(?:(?:[A-Za-z\d\s\_\[\]]+)(?:[=\s][A-Za-z-\[\]\d\s\'\"\_+\\*|~]+)?[,]?)?)+);'
)

@dataclass
class Variable:
    '''
        Variable:
        <type> <name> = <value>, <name> ... ;
    '''
    _type: str
    name: str
    value: str
    is_array: bool = False

    @staticmethod
    def get_all_variables(source: str) -> List['Variable']:
        variables: List[Variable] = []

        offset = 0
        while (variable_declaration := VARIABLE_SEARCH_REGEX.search(source, offset)) is not None:
            groups = variable_declaration.groups()
            statement = groups[0]
            vartype = groups[1]
            var_statement = statement[len(vartype):]

            for variable in var_statement.split(","):
                parts = variable.split("=")
                varname = parts[0].strip()

                if "[" in varname:
                    varname = varname[:varname.index("[")]

                varvalue = None if len(parts) == 1 else parts[1].strip()
                variables.append(Variable(vartype, varname, varvalue))

            offset = variable_declaration.end()
        return variables

    def append_to_all_variable_name(source: str, append: str) -> str:
        """appends text to all the variable name in the source code"""

        # TODO fix cases when variable is inside a string def, those are not variables 

        variables = Variable.get_all_variables(source)
        verboseprint(f"[Variable] found {len(variables)} variable declarations")
        
        for variable in variables:
            replace_with = f"{variable.name}{append}"
            offset = 0
            variable_replace_search = re.compile(fr"({variable.name})\b")
            variable_divider = "()*;+-/~%^&=: <>?|[],"
            string_divider = "\"\'"

            verboseprint(f"[Variable] replace '{variable.name}' with '{replace_with}'")

            while (search := variable_replace_search.search(source, offset)) is not None:
                is_variable = True
                begin, end = search.span()

                variable_name = source[begin:end]
                
                # left
                for i in range(begin - 1, -1, -1):
                    char = source[i]
                    if char in variable_divider:
                        break
                    if char in string_divider:
                        is_variable = False
                        break
                    variable_name = char + variable_name

                # right
                if is_variable:
                    for i in range(end, len(source)):
                        char = source[i]
                        if char in variable_divider:
                            break
                        if char in string_divider:
                            is_variable = False
                            break
                        variable_name = variable_name + char
                
                variable_name = variable_name.strip()
                is_variable = is_variable and variable_name == variable.name
                
                if is_variable:
                    # replace with new variable name
                    source = source[:begin] + replace_with + source[end:]
                        
                offset = search.end()

        return source
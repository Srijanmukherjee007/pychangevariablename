from abc import abstractclassmethod
import re
from typing import List, Tuple
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

    @staticmethod
    def append_to_all_variable_name(source: str, append: str) -> str:
        """appends text to all the variable name in the source code"""

        string_literals = Variable.get_all_string_literals(source)
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
                offset = search.end()
                is_variable = True
                begin, end = search.span()

                for _, s_start, s_end in string_literals:
                    if s_start < begin < s_end and s_start < end < s_end:
                        is_variable = False
                        break        

                if not is_variable:
                    continue

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

                    # update string literal indexes
                    for string_literal in string_literals:
                        if string_literal[1] > begin:
                            string_literal[1] += len(append)
                            string_literal[2] += len(append)
                    

        return source

    @staticmethod
    def get_all_string_literals(sourcecode: str) -> List[List]:
        string_literal_search = re.compile(r'"[^"\\]*(\\.[^"\\]*)*"')
        string_literals = []
        offset = 0
        while (string_literal_match := string_literal_search.search(sourcecode, offset)) is not None:
            start, end = string_literal_match.span()
            string_literals.append([sourcecode[start:end], start, end])
            offset = string_literal_match.end()
        return string_literals
def latex_string_f_operator(fermionop):
  """ Return a LaTeX friendly string of the fermionic operator.

  Args:
    - fermionop (OpenFermion.FermionOperator): Fermionic operator.
  
  Output:
    - (str): Latex friendly string.
  """
  dic = {}
  for operators, coeff in fermionop.terms.items():
    aux = []
    for operator in operators:
      name = ''
      
      if operator[1] == 1:
        name += f'a_{operator[0]}^\dagger'
      else:
        name += f'a_{operator[0]}'

      aux.append(name)
    full_name = ''
    for i in aux:
      full_name += i + ' '
    dic[full_name] = coeff

  output = ''
  for op, coeff in dic.items():
    if coeff > 0:
      output += "+" + str(coeff) + op
    else:
      output += str(coeff) + op
  return output
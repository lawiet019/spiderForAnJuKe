import regex

address = "[ 宁海 宁海 ] 兴海北路"
regionTwo = regex.search(r'(?<=\[\s*)\w+(?=\s)',address).group()
regionThree = regex.search(r'\w+(?=\s*\])',address).group()

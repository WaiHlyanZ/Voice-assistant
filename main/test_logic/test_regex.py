import re

txt = "bla lab idffdfdclose telegram Open telegram cl ose instragam Close twitter close telegram search Elon Aung tell me a story opentheallapplication"
# pattern = r"\s{1}((?:open|close)\s{1}(?:\w+))"
# ['open telegram', 'close instragam', 'close twitter', 'close telegram']
pattern = r"\b(?:open|close)\s(?:\w+)"
if match:= re.findall(pattern, txt, re.IGNORECASE):
    flag = []
    for pair in match:
        action, app = pair.lower().split()
        flag.append((action, app))
    print(flag)
    
from selectolax.lexbor import LexborHTMLParser
import json

with open("raw/all_results.html", "r", encoding="utf-8") as f:
    main_results = f.read()

with open("raw/single_result_example.html", "r", encoding="utf-8") as f:
    single_result = f.read()

tree_main = LexborHTMLParser(main_results)
tree_single = LexborHTMLParser(single_result)



script = tree_main.css(
    'script[data-rh="true"][type="application/ld+json"]'
)[1]

data = json.loads(script.text())
# print(data)

categories = tree_single.css(".css-odhutu")

for category in categories:
    print(category.text())

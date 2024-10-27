import requests
import toml

langs = [("Python", "python"),
         ("Java", "java"),
         ("C++", "cplusplus"),
         ("C", "c"),
         ("JavaScript", "javascript"),
         ("C#", "csharp")]

rooturl = "https://raw.githubusercontent.com/devicons/devicon/refs/heads/master/icons"
svg_dict = {}
for lang_original, lang in langs:
    url = f"{rooturl}/{lang}/{lang}-original.svg"
    r = requests.get(url)
    svg_dict[lang_original] = r.text

toml.dump(svg_dict, open("svg_icons.toml", "w"))

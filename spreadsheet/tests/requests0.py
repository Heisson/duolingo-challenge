from requests_html import HTML, HTMLSession


username = "heiss.on"
username = "IranildaNunes"

spans = HTMLSession().get(
    f"http://duome.eu/{username}",
    headers={
        "Cookie": f"PHPSESSID=4dfcaa82cc994ccc6b18d5f906a197bd",
    },
).html.find("span")

xp = int(spans[1].text.replace(" XP", ""))
streak = int((spans[4] if len(spans) <= 54 else spans[5]).text)

print(f"streak: {streak}\nxp: {xp}")

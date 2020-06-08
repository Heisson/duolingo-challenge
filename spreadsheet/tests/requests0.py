from requests_html import HTML, HTMLSession


# username = "heiss.on"
username = "PedrohSampaioo"

response_html = HTMLSession().get(
    f"http://duome.eu/{username}",
    headers={
        "Cookie": f"PHPSESSID=4dfcaa82cc994ccc6b18d5f906a197bd",
    },
).html

xp = response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[1]", first=True).text
streak = response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]", first=True).text

if "#" in streak:
	streak = response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]/span[1]", first=True).text

print(f"streak: {streak}\nxp: {xp}")

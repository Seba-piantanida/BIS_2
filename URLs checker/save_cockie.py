from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/")
cookies = [
    {'name': 'JSESSIONID', 'value': "ajax:6335637823900184615"},
    {'name': 'bcookie', 'value': "v=2&747001fe-4598-4566-8d05-191a9ddc3a36"},
    {'name': 'bscookie','value': "v=1&202404241243006100f9aa-222a-4463-8c04-71c3f7026485AQExMqp4Qbl6HEu4PuKXY1Kfs843e2WL"},
    {'name': 'dfpfpt','value': '8946ead38e934ccc9621e061a2c7db87'},
    {'name': 'fptctx2','value': 'taBcrIH61PuCVH7eNCyH0Iitb%252bEMfwlgK%252fM8w%252f28Ebe0ETAMOykZ78B0N5lCS4x0QI4d146luzqhvjWRnJdlIMM0JoJVHy70LcqnERHQsQbDyQ7C0Wo7jqXiNDLDRhWK7sNxbM28O9n767MdHrqK5etnsUaoS38%252fnlTyPoAWPJbABQ4oo9EIM3We4522rc6uuxLS9K3gUq%252bKjK1t56vC6iUs1Cg%252fWxf%252fbDATs2Q0HvlTW5h9e%252f7mZgxOLxXm9ySU8MgcousnoomqvMHx5Xz1jT5hLGoQykSR0Vi2YCQNNd%252bm%252fjTR6PLCeYflqX6aQwdmuq%252bplynFCKXC7cta9Eyn25HyzV3r3gy9qmM4FEpNUOI%253d'},
    {'name': 'lang','value': 'v=2&lang=it-it'},
    {'name': 'li_alerts','value': 'e30='},
    {'name': 'li_at','value': 'AQEDAUyWys0DfhYKAAABjxAiwC8AAAGPNC9EL1YAGnsYBaWNst8-OlHc80zb9oQPcYW4nHxoI_gTpsITrfaac4xdMLTu-AkDul_Rla6YPs7mj07St4Fiob3H4K2juNJYWdLCPWpZVU83zlaGTqHUvoNP'},
    {'name': 'li_gc','value': 'MTswOzE3MTM5NjI1ODA7MjswMjFzenwBIzCPsWYnaQOx0iZFAzLB+wcc+5hHG7Nanb2FRg=='},
    {'name': 'li_mc','value': 'MTs0MjsxNzEzOTY0NTM3OzI7MDIx5mZ7a8udMLfN87ViBQLRaBhoPjBMuuNGkmFZyxMdcro='},
    {'name': 'li_theme','value': 'light'},
    {'name': 'li_theme_set','value': 'app'},
    {'name': 'app','value': 'true'},
    {'name': 'true','value': "b=VB33:s=V:r=V:a=V:p=V:g=5905:u=28:x=1:i=1713962664:t=1714046019:v=2:sig=AQExwIApkTXW1x2uMFdGvdAyL5gwrpDq"},
    {'name': 'timezone','value': 'Europe/Rome'},
]

for cookie in cookies:
    driver.add_cookie(cookie)

cookies = driver.get_cookies()

# 3. Salva i cookie in un file
with open("cookies.txt", "w") as f:
    for cookie in cookies:
        f.write(f"{cookie['name']}={cookie['value']}\n")

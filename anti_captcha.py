from anticaptchaofficial.recaptchav2proxyon import *

solver = recaptchaV2Proxyon()
solver.set_verbose(1)
solver.set_key(#insert your anticaptcha developer api key here)
solver.set_website_url("https://www.argos.co.uk/account/login?clickOrigin=header:home:account")
solver.set_website_key("6Le7FS0UAAAAAAW85PV8Rq5iAB2jxn63NBHmdw6K")
solver.set_proxy_address(#proxy address)
solver.set_proxy_port(#proxy port)
solver.set_proxy_login(#proxy username)
solver.set_proxy_password(#proxy password)
solver.set_user_agent("Mozilla/5.0")
solver.set_cookies("test=true")

g_response = solver.solve_and_return_solution()
if g_response != 0:
    print("g-response: "+g_response)
else:
    print("task finished with error "+solver.error_code)


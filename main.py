# Auto Almost Everything
# Youtube Channel https://www.youtube.com/c/AutoAlmostEverything
# Please read README.md carefully before use

# Solve captcha by using https://2captcha.com?from=11528745.

import os, time, zipfile
from datetime import datetime
import urllib.parse as urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Proxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from Modules import update, notification, log, captcha

app = 'FreeBitco.in'
app_path = 'https://freebitco.in'

# Browser config
opts = Options()
opts.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'  # <-- Change to your Chromium browser path, replace '\' with '\\'.
opts.add_experimental_option('excludeSwitches', ['enable-automation'])
opts.add_experimental_option('useAutomationExtension', False)
cap = DesiredCapabilities.CHROME.copy()
cap['platform'] = 'WINDOWS'
cap['version'] = '10'
proxy = 'YourProxy'  # <-- To use proxy, replace 'YourProxy' by proxy string. There are two types: IP:Port or IP:Port:User:Pass
if proxy != '' and proxy != 'YourProxy':
    if len(proxy.split(':')) == 2:
        proxies = Proxy({
            'httpProxy': proxy,
            'ftpProxy': proxy,
            'sslProxy': proxy,
            'proxyType': 'MANUAL',
        })
        proxies.add_to_capabilities(cap)
    elif len(proxy.split(':')) == 4:
        t = proxy.split(':')
        proxy_host = t[0]
        proxy_port = t[1]
        proxy_user = t[2]
        proxy_pass = t[3]
        manifest_json = '''
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                '''
        background_js = '''
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                            singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                            },
                            bypassList: ["localhost"]
                            }
                        };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    ''' % (proxy_host, proxy_port, proxy_user, proxy_pass)
        plugin_file = 'authProxy_%s_%s.zip' % (proxy_host, proxy_port)
        with zipfile.ZipFile(plugin_file, 'w') as zf:
            zf.writestr("manifest.json", manifest_json)
            zf.writestr("background.js", background_js)
        opts.add_extension(plugin_file)
chromedriver_list = ['91', '90', '89', '88', '87']
chromedriver_index = 0
chromedriver_path = '.\\Drivers\\%s.exe' % chromedriver_list[chromedriver_index]

# Account config
fbtc_cookies = [
    {
        'name': 'fbtc_userid',
        # Replace by your user ID -->
        'value': 'YourUserID',
        # <-- Replace by your user ID
        'domain': 'freebitco.in',
        'path': '/',
    },
    {
        'name': 'fbtc_session',
        # Replace by your session -->
        'value': 'YourSession',
        # <-- Replace by your session
        'domain': 'freebitco.in',
        'path': '/',
    },
]

log.screen_n_file('\n\n-+- -A- -U- -T- -O- -+- -A- -L- -M- -O- -S- -T- -+- -E- -V- -E- -R- -Y- -T- -H- -I- -N- -G- -+-',
                  False)
now = datetime.now()
log.screen_n_file('\n Script starts at ' + f'{now:%d/%m/%Y %H:%M:%S}', False)
log.file('Freebitco.in user ID is ' + fbtc_cookies[0]['value'], False)
log.file('Freebitco.in session is ' + fbtc_cookies[1]['value'], False)

# Anti-captcha config
autoCaptcha = True  # <-- Change to True if you want to use 2captcha to solve the captcha.
if autoCaptcha:
    captchaServiceName = '2Captcha'  # <--- 2Captcha, CapMonster, AntiCaptcha
    # Replace by your API Key -->
    ac = captcha.Captcha(captchaServiceName, 'YourAPIKey')
    # <-- Replace by your API Key
    log.file(captchaServiceName + ' API Key is ' + ac.getAPIKey(), False)


# Choose webdriver version
def changeDriver():
    global chromedriver_index, chromedriver_path
    if chromedriver_index + 1 <= len(chromedriver_list) - 1:
        chromedriver_index += 1
        chromedriver_path = '.\\Drivers\\%s.exe' % chromedriver_list[chromedriver_index]
        return True
    return False


# Get with exception handler
def get(browser, url):
    try:
        browser.get(url)
    except:
        pass


# Roll for BTC
def Roller():
    func = "Roll"
    func_path = '/?op=home'

    while True:
        log.screen_n_file('', False)
        log.screen_n_file(func.upper())

        while True:
            try:
                browser = webdriver.Chrome(desired_capabilities=cap, options=opts,
                                           executable_path=chromedriver_path)
                log.screen_n_file(
                    '[*] Decide to choose web driver version %s to run.' % chromedriver_list[chromedriver_index])
                break
            except Exception as ex:
                if 'This version of ChromeDriver only supports' in str(ex):
                    log.screen_n_file(
                        '[*] Web driver version %s is not supported your browser. Switching to other web driver...' %
                        chromedriver_list[chromedriver_index])
                    if not changeDriver():
                        log.screen_n_file(
                            '[!] All of web drivers are not supported your browser. Please update browser or download web driver.')
                        time.sleep(999999)
                else:
                    log.screen_n_file('[!] %s has exception: %s!' % (app, ex))
                    notification.notify(app, '%s has exception: %s!' % (app, ex))

        browser.set_page_load_timeout(60)
        browser.implicitly_wait(60)
        try:
            get(browser, app_path)
            for cookie in fbtc_cookies:
                browser.add_cookie(cookie)
            get(browser, app_path + func_path)
            while True:
                time.sleep(1)
                try:
                    browser.find_elements_by_xpath("//iframe[contains(@title, 'reCAPTCHA')]")[0]
                except:
                    continue
                break
            if '<div id="wait" align="center" style="display:none;">' not in browser.page_source:
                log.screen_n_file('[*] Waiting for the next claim...')
                notification.notify(app, 'Waiting for the next claim...')
                while '<div id="wait" align="center" style="display:none;">' not in browser.page_source:
                    time.sleep(1)

            try:
                browser.execute_script('document.getElementsByClassName("cc_banner")[0].remove();')
            except:
                pass
            try:
                browser.execute_script('document.getElementsByClassName("reveal-modal-bg")[0].remove();')
            except:
                pass

            while True:
                try:
                    time.sleep(0.2)
                    if autoCaptcha:
                        log.screen_n_file('[+] Automatically solve captcha.')
                        recaptcha = browser.find_elements_by_xpath("//iframe[contains(@title, 'reCAPTCHA')]")[0]
                        sitekey = ''
                        for query in urlparse.urlparse(recaptcha.get_attribute('src')).query.split('&'):
                            if 'k=' in str(query):
                                sitekey = str(query).split('=')[1]
                        token = ac.reCaptcha(sitekey, browser.current_url)
                        log.screen_n_file('  [+] Captcha response is %s.' % (token[:7] + '...' + token[-7:]))

                        # Run callback function
                        browser.execute_script('''
                            document.getElementById("g-recaptcha-response").innerHTML=arguments[0];
                        ''', token)
                        time.sleep(2)
                        browser.find_element_by_xpath("//input[contains(@id, 'free_play_form_button')]").click()
                        time.sleep(10)
                        break
                    else:
                        log.screen_n_file('[+] Manually solve captcha.')
                        notification.sound()
                        notification.notify(app, 'Please solve captcha!')
                        time.sleep(60)
                        break
                except Exception as ex:
                    print(ex)
                    pass
            log.screen_n_file('[+] Rolled. Wait for 1 hour to roll again.')
            browser.quit()
            time.sleep(3600)
        except Exception as ex:
            log.screen_n_file('[!] %s has exception: %s!' % (app, ex))
            notification.notify(app, '%s has exception: %s!' % (app, ex))


if update.check():
    log.screen_n_file('[*] New version is released. Please download it! Thank you.')
    notification.notify(app, 'New version is released. Please download it! Thank you.')
    os.system('start https://www.youtube.com/watch?v=P2apjv1qhm8')
else:
    Roller()

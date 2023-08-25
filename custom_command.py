
from datetime import datetime
from setup import getConfig, getMode
from Ops import LocalStorage, editLogQueue, visitLogNew, visitLogUpdate
import logging
import os
import json
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

from openwpm.commands.types import BaseCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.socket_interface import ClientSocket
import time


from cookieButton_rules import commons, rules
from cookieButton_button_signatures import accept_button_list


import builtins
builtins.cookieButtons = {} 
builtins.localStorage={} 

class InstallExtension(BaseCommand):
    def __init__(self) -> None:
        self.logger = logging.getLogger("openwpm")

    def __repr__(self) -> str:
        return "InstallExtension"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        ext_path = os.getcwd() + "/resources/extensions/"
        mode = getMode()
        browser_config = mode.split('_')[1]

        if browser_config == 'omaticno':
            ext_path = ext_path + "consent_o_matic-1.0.8.xpi"
            webdriver.install_addon(ext_path)

        if browser_config == 'omaticall':
            ext_path = ext_path + "consent_o_matic-accept_all_1.0.8.xpi"
            webdriver.install_addon(ext_path)

        if browser_config == 'dontcare':
            ext_path = ext_path + "i_dont_care_about_cookies-3.4.2.xpi"
            webdriver.install_addon(ext_path)

        if browser_config == 'ninja':
            ext_path = ext_path + "ninja_cookie-0.2.7.xpi"
            webdriver.install_addon(ext_path)

        if browser_config == 'cookieblock':
            ext_path = ext_path + "cookieblock-1.1.0.xpi"
            webdriver.install_addon(ext_path)

        if browser_config == 'superagent':
            ext_path = ext_path + "super_agent-2.6.0.xpi"
            webdriver.install_addon(ext_path)

     
       



class DoInteraction(BaseCommand):
    def __init__(self) -> None:
        self.logger = logging.getLogger("openwpm")

    # While this is not strictly necessary, we use the repr of a command for logging
    # So not having a proper repr will make your logs a lot less useful
    def __repr__(self) -> str:
        return "DoInteraction"

    # Have a look at openwpm.commands.types.BaseCommand.execute to see
    # an explanation of each parameter
    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait

        

        
        element_id = 'body'  
        try:
            webdriver.find_element_by_css_selector(
            element_id).send_keys(Keys.PAGE_DOWN)
        except:
            element_id = 'html'
        try:
            # simulate human interactions
            webdriver.find_element_by_css_selector(
                element_id).send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            webdriver.find_element_by_css_selector(
                element_id).send_keys(Keys.PAGE_DOWN)
            time.sleep(0.7)
            webdriver.find_element_by_css_selector(
                element_id).send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            webdriver.find_element_by_css_selector(
                element_id).send_keys(Keys.TAB)
            time.sleep(0.4)
            webdriver.find_element_by_css_selector(
                element_id).send_keys(Keys.TAB)
            time.sleep(0.4)
            webdriver.find_element_by_css_selector(
                element_id).send_keys(Keys.TAB)
            time.sleep(0.5)
            webdriver.find_element_by_css_selector(
                element_id).send_keys(Keys.END)
            time.sleep(1.3)
        except:
            pass



class LoadMobileConfigs(BaseCommand):
    def __init__(self) -> None:
        self.logger = logging.getLogger("openwpm")

    def __repr__(self) -> str:
        return "LoadMobileConfigs"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        webdriver.set_window_size(360, 760)



class CopyLocalStorage(BaseCommand):
    def __init__(self, siteID) -> None:
        self.logger = logging.getLogger("openwpm")
        self.siteID=siteID

    def __repr__(self) -> str:
        return "CopyLocalStorage"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        import shutil
        time.sleep(2)
        source=webdriver.capabilities['moz:profile'] + '/webappsstore.sqlite'
        dist= "./profiles/openwpm/" + str(self.siteID) + "/webappsstore.sqlite"

        try:
            shutil.copyfile(source, dist)
        except Exception as e:
            print(str(e))




class LoadLocalStorage(BaseCommand):
    def __init__(self, siteID) -> None: 
        self.logger = logging.getLogger("openwpm")
        self.site_id=siteID

    def __repr__(self) -> str:
        return "LoadLocalStorage"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:

        # webdriver.execute_script("return window.localStorage;")
        storage = LocalStorage(webdriver)

        #import builtins
        #builtins.localStorage[self.site_id]=storage 
 
        filePath = str(manager_params.data_directory.absolute()
                       ) + "/localStorage.txt"

        with open(filePath, 'w') as f:
            print(storage, file=f)  
         

class LogVisit(BaseCommand):
    def __init__(self, p_queue, p_site_id, p_site_url, p_subpage_id, p_ops) -> None:
        self.logger = logging.getLogger("openwpm")
        self.p_queue = p_queue
        self.p_site_id = p_site_id
        self.p_site_url = p_site_url
        self.p_subpage_id = p_subpage_id
        self.p_ops = p_ops

    def __repr__(self) -> str:
        return "LogVisit"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        if self.p_ops == 0:
            str()#visitLogNew(self.p_site_id, self.p_site_url, self.p_subpage_id,)
        else:
            str()#visitLogUpdate(self.p_site_id, self.p_subpage_id, self.p_ops)
            # editLogQueue(self.p_queue,self.p_site_id,self.p_subpage_id,self.p_ops, datetime.now()) #p_queue, p_site_id, p_subpage_id, p_ops, p_value
            #print('self.p_subpage_id', self.p_subpage_id)


class ChangeRes(BaseCommand): 

    def __init__(self) -> None:
        self.logger = logging.getLogger("openwpm")
 
    def __repr__(self) -> str:
        return "ChangeRes"
 
    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:   
    
        resolution= getConfig('resolution') 
        webdriver.set_window_size(resolution[0], resolution[1])



class DetectBannerCommand(BaseCommand):
    """
    command to detect the cookie banner and the accept-all button of a specific website.

    :return: nothing
    """

    # init method to initialize logger
    def __init__(self, domain, siteID) -> None:
        self.logger = logging.getLogger("openwpm")
        # get domain from caller
        self.domain = domain
        # set selenium webdriver for finding html elements
        self.webdriver = None
        # bool if site has button or banner
        self.has_cookie_options = False
        self.site_id=str(siteID)


    # While this is not strictly necessary, we use the repr of a command for logging
    # So not having a proper repr will make the logs a lot less useful
    def __repr__(self) -> str:
        return "DetectBannerCommand"

    # Have a look at openwpm.commands.types.BaseCommand.execute to see
    # an explanation of each parameter
    def execute(
            self,
            webdriver: Firefox,
            browser_params: BrowserParams,
            manager_params: ManagerParams,
            extension_socket: ClientSocket,
    ) -> None:  

        # log current url
        current_url = webdriver.current_url

        import builtins
        builtins.cookieButtons[self.site_id]  = { 
            "AcceptAllFired": None,
            "FoundSignature": None,
            "FoundSignatureParent": None,
            "ButtonPosition": {
                "x": None,
                "y": None,
                "width": None,
                "height": None
            },
            "FireTime":None
        }  
        self.logger.info(f'({self.domain}) Current URL is: {current_url}')
        # set the web driver for further use
        self.webdriver = webdriver
        # find banner by calling the method 
        time.sleep(2) # s. related work 6. footnote: Do Cookie Banners Respect my Choice? Measuring Legal Compliance of Banners from IAB Europe’s Transparency and Consent Framework

        self.find_and_click_accept_button()
        if(builtins.cookieButtons[self.site_id]["AcceptAllFired"]):
            time.sleep(3) 
            
            from DBOps import DBOps
            db = DBOps()
            import base64
            query="UPDATE sites SET log_customall='" + base64.b64encode(str(builtins.cookieButtons[self.site_id]).encode('ascii')).decode('ascii')   +"' where id=" + str(self.site_id)
            db.exec(query)
        
        filePath = str(manager_params.data_directory.absolute()
                       ) + "/log_customall.txt"

        with open(filePath, 'w') as f:
            print(builtins.cookieButtons[self.site_id], file=f) 
        

    def find_and_click_accept_button(self):
        """
        method to find and click the accept-all button (if present), which sets all cookies. Furthermore, the position
        will be logged.

        :return: nothing.
        """ 
        # get a list of "button" web elements
        # either tag, id, type or role should be "button"
        all_buttons_list = \
            self.webdriver.find_elements(By.TAG_NAME, 'button') + \
            self.webdriver.find_elements(By.ID, 'button') + \
            self.webdriver.find_elements_by_xpath("//*[@type='button']") + \
            self.webdriver.find_elements_by_xpath("//*[@role='button']")
        for button in all_buttons_list:
            if button.text:
                # local variable containing the string inside the button
                button_text = button.text
                # if the lowercase text of the button matches with the rule, accept-all button is found
                if str(button_text).lower() in accept_button_list:
                    # verify that the button is for cookies
                    # default recursion depth is 5
                    if not self.verify_button(button, 5):
                        # skip this button
                        continue
                    # log the position and the signature
                    builtins.cookieButtons[self.site_id]["FoundSignature"]  = button_text
                    
                    builtins.cookieButtons[self.site_id]["ButtonPosition"]  = button.rect
                    acceptAllFired=False
                    self.logger.info(f'({self.domain}) Button at: {button.rect}')
                    self.logger.info(f'({self.domain}) Signature: {str(button_text).lower()}')
                    
                    # try to click the matching web element
                    try:
                        button.click()
                        # log the success
                        self.logger.info(f'({self.domain}) Button "{button_text}" clicked!')
                        acceptAllFired=True

                        builtins.cookieButtons[self.site_id]["FireTime"] = datetime.now()

                    # Ignore StaleElementsReferenceException
                    except StaleElementReferenceException:
                        pass
                    # when selenium webdriver click failed, try to click with javascript
                    except (ElementClickInterceptedException, ElementNotInteractableException):
                        try:
                            # execute a minimal javascript function
                            # click button by passing it as an argument
                            self.webdriver.execute_script("arguments[0].click();", button)
                            # log the success
                            self.logger.info(f'({self.domain}) Button "{button_text}" clicked!')
                            acceptAllFired=True 
                            builtins.cookieButtons[self.site_id]["FireTime"] = datetime.now()
                        except Exception as error:
                            self.logger.error(f'({self.domain}) {error}')
                    # log error
                    except Exception as error:
                        self.logger.error(f'({self.domain}) {error}')
                    # set the bool because button was found
                    builtins.cookieButtons[self.site_id]["AcceptAllFired"]=acceptAllFired
                    self.has_cookie_options = True
                    # end loop
                    break
        if not self.has_cookie_options:
            # try to find a cookie banner instead
            self.find_banner()
        # clear list
        all_buttons_list.clear()

    def verify_button(self, current_element, depth):
        """
        recursive method to verify if a button web element is related to cookies.

        :param current_element: web element to verify. Initial element is a button.
        :param depth: number to limit the recursion depth. Default is 5.
        :return: True if cookie string was found, otherwise False.
        """
        """    
        # set the button element as child
        current_element = button
        # iterate until reaching head of document (<html ... \html>)
        while not str(current_element.tag_name) == "html":
            if current_element.text:
                # if string cookie in web element, button is cookie related
                if "cookies" in str(current_element.text).lower():
                    self.logger.info(f'({self.domain}) String "cookies" found in parent element')
                    # return true
                    return True
            # next element is parent of child
            parent_element = current_element.find_element(By.XPATH, "./..")
            current_element = parent_element
        # button has no parent with cookie string
        return False
        """
        # check if depth limit or html head is reached
        if depth == 0 or str(current_element.tag_name) == "html":
            # end recursion, return false so button couldn't be validated
            return False
        # enter recursive checking
        else:
            # set the new parent element
            # in first recursion step the direct parent of button is parent element
            # example: button is at html/body/div/span/button
            # parent in first recursion step would be html/body/div/span in example
            parent_element = current_element.find_element(By.XPATH, "./..")
            # get all child elements from parent element
            # child elements in first recursion step would be html/body/div/span/* in example
            child_elements = parent_element.find_elements(By.XPATH, ".//*")
            # iterate through the child elements to find cookie relation
            for child_element in child_elements:
                # only check if element has a displayed text
                if child_element.text:
                    # iterate through a list to identify relation ( https://github.com/RUB-SysSec/we-value-your-privacy/blob/master/privacy_wording.json)
                    privacy_words=[ "cookies", "privacy", "gdpr", "datenschutz", "datenrichtlinie", "privatssphäre", "datenschutzbestimmungen",  "datenschutzrichtlinie","privatësia", "politika e të dhënave",  "konfidencialiteti", "politikat e privatësisë", "politikat e privatesise", "mbrojtja e të dhënave", "gegevensbeleid", "confidentialité", "politique d’utilisation des données", "privacybeleid", "условия за ползване", "поверителност", "политика за данни", "политика за бисквитки", "условия", "privacidade", "política de dados", "data policy", "隐私权政策", "数据使用政策", "私隱政策", "數據使用政策", "gizlilik", "veri i̇lkesi", "απόρρητο", "πολιτική δεδομένων", "soukromí", "soukromi", "zásady používání dat", "ochrana soukromí", "podmínky", "ochrana dat", "ochrana udaju", 
                    "ochrana osobních údajů", "datenschutzrichtlinie", "beskyttelse af personlige oplysninger", "datapolitik", "cookiepolitik", "privatlivspolitik", "personoplysninger", "regler om fortrolighed", "personlige data", "privaatsus", "kasutustingimused", "isikuandmete", "isikuandmete töötlemise", "küpsised", "konfidentsiaalsuse", "andmekaitsetingimused", "الخصوصية", "سياسة البيانات", "privacidad", "política de datos", "protecció de dades", "aviso legal", "yksityisyys", "tietokäytäntö", "tietosuojakäytäntö", "yksityisyyden suoja", "tietosuojaseloste", "rekisteriseloste", "tietosuoja", "yksityisyydensuoja", "persónuvernd", "normativa sui dati", "privatumas", "slapukai", "privatumo", "privātums", "privātuma", "sīkdatņu", "sīkdatne", "приватност", "политика о подацима", "privatnost", "privatezza", "personvern", "retningslinjer for data", "prywatność", "prywatnosci", "zasady dotyczące danych", "prywatności", "confidențialitate", "politica de utilizare", "cookie-uri", "confidentialitate", "cookie-urilor", "protecţia datelor", "конфиденциальность", "политика использования данных", "политика конфиденциальности", "политика обработки персональных данных", "sekretess", "datapolicy", "personuppgifter", "webbplatsen", "integritetspolicy", "zasebnost", "piškotkih", "varstvo podatkov", "ochrana súkromia", "zásady využívania údajov", "ochrana údajov", "ochrana osobných údajov", "súkromie", "piškotki", "zásady ochrany osobných", "osobné údaje", "ochrany osobných údajov", "veri politikası", "kvkk", "kişisel verilerin korunması", "конфіденційність", "policy"]

                    for signature in privacy_words:
                        # if string cookie is in web element, button is cookie related
                        if signature in str(child_element.text).lower():
                            # log that a cookie string was found in one of parental elements
                            self.logger.info(f'({self.domain}) String "{signature}" found in parent element')
                            
                            builtins.cookieButtons[self.site_id]["FoundSignatureParent"]=signature
                            # return true
                            return True
            # try find it on next parental level (depth - 1)
            return self.verify_button(parent_element, depth - 1)

    def find_banner(self):
        """
        method to find the cookie banner.

        :return: nothing.
        """
        # first check the rules
        for rule_key, rule_value in rules.items():
            # if domain in rule, then check values for signature
            if self.domain == rule_key:
                for letter, signature in rule_value.items():
                    # signature is under letter "s": {..., example.com: {"j": 0, "s": #cookie}, ...}
                    if letter == "s":
                        self.find_matches(signature)
                        break
                    else:
                        # try to find banner by common pattern
                        for common_signature in commons.values():
                            # try commons until first match
                            if not self.has_cookie_options:
                                self.find_matches(common_signature)
        if not self.has_cookie_options:
            # nothing found, so log result
            self.logger.info(f'({self.domain}) No Button/Banner found')

    def find_matches(self, signature):
        """
        method to determine if a css-signature of the idcac (i don't care about cookies)-plugin matches
        with the signature of the banner. Furthermore the position will be logged.

        :param signature: css-signature from the plugin.
        :return: nothing.
        """
        # remove display:none !important
        fixed_signature = signature.replace("{display:none !important}", "")
        # put it in a list for checking
        css_signature_list = []
        if fixed_signature.find(",#") != -1:
            # can have multiple elements
            css_signature_list = fixed_signature.split(",")
        else:
            css_signature_list.append(fixed_signature)
        # now try to find signature in html
        for css_signature in css_signature_list:
            # signatures are in css shape
            try:
                # get a list of web elements matching the signature
                matched_web_elements = self.webdriver.find_elements(By.CSS_SELECTOR, css_signature)
                if matched_web_elements:
                    for matched_web_element in matched_web_elements:
                        # if text is set, print
                        if matched_web_element.text:
                            # log the position and the signature
                            self.logger.info(f'({self.domain}) Banner at: {matched_web_element.rect}')
                            self.logger.info(f'({self.domain}) Signature: {css_signature}')
                            # set the bool and break the loop
                            self.has_cookie_options = True
            # ignore NoSuchElements
            except NoSuchElementException:
                pass
            except Exception as error:
                self.logger.error(f'({self.domain}) {error}')




class TMP(BaseCommand):
    def __init__(self, siteID) -> None:
        self.logger = logging.getLogger("openwpm")
        self.site_id=siteID

    def __repr__(self) -> str:
        return "LoadLocalStorage"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
 
        print(builtins.localStorage[self.site_id])

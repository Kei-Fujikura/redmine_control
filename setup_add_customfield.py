# -*-coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class RedmineSetup:
    """
        it is redmine Initial setup class
    """
    def __init__(self, url_top="http://localhost:8080/redmine"):
        """
            init PhantomJS webdriver and TopURL
        """
        self.wd = webdriver.PhantomJS()
        self.snapshot_cnt = 0
        self.TOP_URL = url_top

    def __ErrPrint(self, e, name):
        print("Error: " + name)
        print("type: " + str(type(e)))
        print("args: " + str(e.args))
        print("error:¥r¥n" + str(e))

    def __snapshot(self, name="shot"):
        """
            get snapshot
            its called on __getpage method
        """
        try:
            cnt = str(self.snapshot_cnt)
            self.wd.save_screenshot(".¥¥e¥¥"+name+cnt+".png")
            self.snapshot_cnt += 1
        except Exception as e:
            self.__ErrPrint(e, "snapshot")

    def __getpage(self, url, name=""):
        self.wd.get(url)
        time.sleep(3)
        self.__snapshot(name)

    def open_and_login(self, name, passwd):
        """
            Open toppage and Login to redmine
        """
        loginurl = self.TOP_URL+"/login"
        try:
            self.__getpage(loginurl, "open_and_login_1_")
            try:
                self.wd.find_element(by='class', value="logout").click()
            except:
                pass

            try:
                self.__getpage(loginurl, "open_and_login_2_")
                self.wd.find_element(by='id', value="username").send_keys(name)
                self.wd.find_element(by='id', value="password").send_keys(passwd)
                self.wd.find_element(by='name', value="login").click()
                self.__getpage(loginurl, "open_and_login_3_")
                self.__snapshot("open_and_login")
            except:
                print(":::Error")
                raise Exception
        except Exception as e:
            self.__ErrPrint(e, "open_and_login")

    def add_customfield(self, name, param=None):
        """
            Add CustomTicketField
            now, add text field only.
        """
        show_cs = self.TOP_URL+"/custom_fields"
        add_newurl = self.TOP_URL+"/custom_fields/new?type=IssueCustomField"

        # set name
        try:
            csname = "custom_field[name]"
            self.__getpage(add_newurl, "add_new_cf")
            self.wd.find_element(by="name", value=csname).send_keys(name)
        except Exception as e:
            self.__ErrPrint(e, "add_customfield")

        if param is not None:
            # set format
            self.__select_cs_format(param)

            # set required
            self.__select_cs_required(param)

            # set forall
            self.__select_cs_forall(param)

        # commit
        self.wd.find_element(by="name", value="commit").click()
        self.__getpage(show_cs, "added_cf")

    def __del__(self):
        """
            Quit PhantomJS browser
        """
        self.wd.quit()

    def __select_cs_format(self, param):
        """
            select format type
        """
        if param.get('fmt') is not None:
            print("field_format: %s"%(param.get('fmt')))
            el = self.wd.find_element(by="id", value="custom_field_field_format")
            arrow_cnt = 0
            if param["fmt"] == "int":
                arrow_cnt = 2
            elif param["fmt"] == "float":
                arrow_cnt = 3

            for x in range(arrow_cnt):
                el.send_keys(Keys.ARROW_DOWN)

            el.send_keys(Keys.ENTER)

    def __select_cs_required(self, param):
        if param.get('required') is True:
            print("is_required")
            el = self.wd.find_element(by="id", value="custom_field_is_required")
            el.click()

    def __select_cs_forall(self, param):
        if param.get('forall') is True:
            print("for_all")
            el = self.wd.find_element(by="id", value="custom_field_is_for_all")
            el.click()

if __name__ == "__main__":
    url_top = "http://fj-prg.cloudapp.net/redmine"
    rc = RedmineSetup(url_top)
    rc.open_and_login(name="user", passwd="bitnami")
#    rc.add_customfield("sample11", {"fmt": "int"})
    rc.add_customfield("sample13", {"fmt": "float", "forall": True, "required": True})

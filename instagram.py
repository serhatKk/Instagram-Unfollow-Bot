from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from os import system
from getpass import getpass
from colorama import Fore, Style

class Instagram():
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=options)
        self.url = "https://www.instagram.com/"
        self.username = ""
        self.password = ""
        self.followers_info = []
        self.following_info = []
        self.unfollowers_info = []
        self.isLoggedIn = False
        self.isGetFollowers = False
        self.isGetFollowing = False
        self.isGetUnfollowers = False   

    def signIn(self):
        if (self.isLoggedIn):
            system("cls")
            print(Fore.GREEN+'Already logged in'+Style.RESET_ALL)

        else:
            system("cls")
            self.username = input('Username: ')
            self.password = getpass()
            system("cls")
            self.driver.get(self.url)
            time.sleep(2)
            while True:
                username = self.driver.find_element(By.XPATH, "//input[@name='username']")
                password = self.driver.find_element(By.XPATH, "//input[@name='password']")
                username.send_keys(self.username)
                password.send_keys(self.password)
                password.send_keys(Keys.ENTER)
                time.sleep(7) 
                try:
                    button = self.driver.find_element(By.XPATH,"//button[@class=' _acan _acap _acas _aj1- _ap30']/div")
                    if button.text == "Log In":
                        system("cls")
                        print(Fore.RED+"Incorrect username or password. Please try again!"+Style.RESET_ALL)
                        username.send_keys(Keys.CONTROL + "a")
                        username.send_keys(Keys.DELETE)
                        password.send_keys(Keys.CONTROL + "a")
                        password.send_keys(Keys.DELETE)
                        self.username = input('Username: ')
                        self.password = getpass()
                       
                    else:
                        break
                except:                        
                    self.isLoggedIn = True
                    break                                                
 
    def getFollowers(self):
        if(self.isLoggedIn and self.isGetFollowers==False):
            self.driver.get(self.url + self.username + "/followers")
            time.sleep(3)
            last_height = 0
            followers_list = self.driver.find_element(By.CLASS_NAME, '_aano')
            while True:
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", followers_list)
                time.sleep(3)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight;", followers_list)
                if new_height == last_height:
                    break
                last_height = new_height

            list_element = self.driver.find_element(By.CLASS_NAME, '_aano').find_elements(By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")
            follower_count = 0
            for element in list_element:
                self.followers_info.append({
                    'name': element.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'span').text,
                    'url': element.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'a').get_attribute('href')
                })     
                follower_count += 1
            self.isGetFollowers = True 
            system("cls")
            print(Fore.GREEN+'Process Completed'+Style.RESET_ALL)
        else:
            if(self.isLoggedIn == False):
                system("cls")
                print(Fore.RED+'Please log in first'+Style.RESET_ALL)
            elif(self.isLoggedIn and self.isGetFollowers == False):
                system("cls")
                print(Fore.GREEN+'Please get the followers list first.!'+Style.RESET_ALL)
            else:
                system("cls")
                print(Fore.GREEN+'You already have this list'+Style.RESET_ALL)
        
    def getFollowing(self):
        if(self.isLoggedIn and self.isGetFollowing == False):
            self.driver.get(self.url + self.username + "/following")
            time.sleep(3)
            following_list = self.driver.find_element(By.CLASS_NAME, '_aano')
            last_height = 0
            while True:
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", following_list)
                time.sleep(3)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight;", following_list)
                if new_height == last_height:
                    break
                last_height = new_height

            list_element = self.driver.find_element(By.CLASS_NAME, '_aano').find_elements(By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")
            following_count = 0
            for element in list_element:
                self.following_info.append({
                    'name': element.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'span').text,
                    'url': element.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'a').get_attribute('href')
                })
                following_count += 1
            self.isGetFollowing = True
            system("cls")
            print(Fore.GREEN+'Process Completed'+Style.RESET_ALL)

        else:
            if(self.isLoggedIn == False):
                system("cls")
                print(Fore.RED+'Please log in first'+Style.RESET_ALL)
            elif(self.isLoggedIn and self.isGetFollowing == False):
                system("cls")
                print(Fore.RED+'Please get the list of users you are following first!'+Style.RESET_ALL)
            else:
                system("cls")
                print(Fore.GREEN+'You already have this list'+Style.RESET_ALL)
        
    def findUnfollowers(self):
        if(self.isLoggedIn == True and self.isGetFollowers == True and self.isGetFollowing == True):
            self.unfollowers_info = [user for user in self.following_info if user not in self.followers_info]
            system("cls")
            print(Fore.CYAN+'\nUsers Not Following Back'.center(10, '*')+Style.RESET_ALL)
            index = 1
            for user in self.unfollowers_info:
                print(f"{index}-) {user['name']}")
                index += 1
            self.isGetUnfollowers = True
            print(Fore.GREEN+f'Number of Users Not Following Back: {len(self.unfollowers_info)}'+Style.RESET_ALL)
        elif(self.isGetFollowers and self.isGetFollowing == False):
            system("cls")
            print(Fore.RED+'You need to get the list of users you are following first!'+Style.RESET_ALL)
        elif(self.isGetFollowing and self.isGetFollowers == False):
            system("cls")
            print(Fore.RED+'You need to get the followers list first!'+Style.RESET_ALL)
        elif(self.isLoggedIn == False):
            system("cls")
            print(Fore.RED+'You need to log in first!'+Style.RESET_ALL)
        else:
            system("cls") 
            print(Fore.RED+'You need to get both the followers and following lists first'+Style.RESET_ALL)
    
    def unfollow(self):
        if self.isGetUnfollowers:
            exit_program = False
            for user in self.unfollowers_info:
                while True:
                    choice = int(input(Fore.MAGENTA+f"Username: {user['name']} Do you want to unfollow this user?"+Style.RESET_ALL+"\n1-) Yes\n2-) No\n3) Exit\nChoice: "))   
                    if choice == 1:
                        self.driver.get(user['url'])
                        time.sleep(3)
                        self.driver.find_element(By.XPATH, "//button[@type='button']").click()
                        time.sleep(2)
                        self.driver.find_element(By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 xw2csxc x1odjw0f x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div[8]/div[1]").click()
                        del self.following_info[self.following_info.index({'name': user['name'], 'url': user['url']})]
                        del self.unfollowers_info[self.unfollowers_info.index({'name': user['name'], 'url': user['url']})]
                        break
                    elif choice == 2:
                        break 
                    elif choice == 3:
                        exit_program = True
                        break 
                    else:
                        print(Fore.RED+"Invalid choice. Please try again."+Style.RESET_ALL)

                if exit_program:
                    break  
                        
        else:
            system("cls")
            print(Fore.RED+"Please click on the Show Unfollow List button first"+Style.RESET_ALL)
    
    def unfollowMulti(self):
        if self.isGetUnfollowers:
            self.findUnfollowers()
            print(Fore.CYAN+"\nSeparate numbers with commas example(1,32,28,30,12)"+Style.RESET_ALL)
            number_list = [int(number) - 1 for number in input("Which indexed users do you want to unfollow: ").split(",")]
            for i in number_list:
                self.driver.get(self.unfollowers_info[i]['url'])
                time.sleep(3)
                self.driver.find_element(By.XPATH,"//button[@type='button']").click()
                time.sleep(2)
                self.driver.find_element(By.XPATH,"//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 xw2csxc x1odjw0f x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div[8]/div[1]").click()
                time.sleep(2)
                del self.following_info[self.following_info.index({'name': self.unfollowers_info[i]['name'], 'url':self.unfollowers_info[i]['url']})]

            self.unfollowers_info = [element for index, element in enumerate(self.unfollowers_info) if index not in number_list]

        else:
            system("cls")
            print(Fore.RED+"Please click on the Show Unfollow List button first"+Style.RESET_ALL)        

    def displayFollowers(self):
        if(self.isGetFollowers):
            print(Fore.CYAN+'\nList of Users Following You:'+Style.RESET_ALL)
            for user in self.followers_info:
                print(f"Name : {user['name']}")
            print(Fore.CYAN+f'Total Number of Followers: {len(self.followers_info)}'+Style.RESET_ALL)
        else:
            system("cls")
            print(Fore.RED+'\nPlease click on the Get Followers List option first'+Style.RESET_ALL)
    
    def displayFollowing(self):
        if(self.isGetFollowing):
            print(Fore.CYAN+'\nList of Users You Are Following:'+Style.RESET_ALL)
            for user in self.following_info:
                print(f"Name : {user['name']}")
            print(f'Number of Users Following You: {len(self.following_info)}')
        else:
            system("cls")
            print(Fore.RED+'\nPlease click on the Get Following List option first'+Style.RESET_ALL)
    
    def Menu(self):
        while True:
            print(Fore.YELLOW+'\nMain Menu\n'+Style.RESET_ALL+'1-) Log In\n2-) Get Followers List\n3-) Get Following List\n4-) Show Unfollow List\n5-) Unfollow Users\n6-) Multi Unfollow\n7-) Show Followers\n8-) Show Following\n9-) Exit')
            choice = int(input(Fore.YELLOW+'Choice: '+Style.RESET_ALL))
            if choice == 1:
                self.signIn()
            elif choice == 2:
                self.getFollowers()
            elif choice == 3:
                self.getFollowing()
            elif choice == 4:
                self.findUnfollowers()
            elif choice == 5:
                self.unfollow()
            elif choice == 6:
                self.unfollowMulti()
            elif choice == 7:
                self.displayFollowers()
            elif choice == 8:
                self.displayFollowing()
            elif choice == 9:
                break
            else:
                print(Fore.RED+'Invalid choice. Please try again.'+Style.RESET_ALL)


insta = Instagram()
insta.Menu()

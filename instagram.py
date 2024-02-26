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
        self.unfollowers_info=[]
        self.unfollowers_info_1=[]
        self.isLoggedIn=False
        self.isGetFollowers=False
        self.isGetFollowing=False
        self.isGetUnfollowers=False   

    def signIn(self):
        if (self.isLoggedIn):
            system("cls")
            print(Fore.GREEN+'Giriş yaptınız'+Style.RESET_ALL)

        else:
            system("cls")
            self.username=input('Kullanıcı Adı: ')
            self.password=getpass()
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
                    if button.text == "Giriş yap":
                        system("cls")
                        # Buton bulunduysa, kullanıcı adı veya şifre hatalıdır
                        print(Fore.RED+"Kullanıcı adı veya şifre hatalı. Tekrar deneyin!"+Style.RESET_ALL)
                        username.send_keys(Keys.CONTROL + "a")
                        username.send_keys(Keys.DELETE)
                        password.send_keys(Keys.CONTROL + "a")
                        password.send_keys(Keys.DELETE)
                        self.username = input('Kullanıcı Adı: ')
                        self.password = getpass()
                       
                    else:
                        break
                except:                        
                    self.isLoggedIn=True
                    break                                                
 
    def getFollowers(self):
        if(self.isLoggedIn and self.isGetFollowers==False):
            self.driver.get(self.url+self.username+"/followers")
            time.sleep(3)
            last_height = 0
            followers_list=self.driver.find_element(By.CLASS_NAME,'_aano')
            while True:
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", followers_list)
                time.sleep(3)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight;", followers_list)
                if new_height == last_height:
                    break
                last_height = new_height

            liste = self.driver.find_element(By.CLASS_NAME,'_aano').find_elements(By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")
            takipciSayisi = 0
            for i in liste:
                self.followers_info.append({
                    'name':i.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'span').text,
                    'url':i.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'a').get_attribute('href')
                    })     
                takipciSayisi += 1
            self.isGetFollowers=True 
            system("cls")
            print(Fore.GREEN+'İşlem Tamamlandı'+Style.RESET_ALL)
        else:
            if(self.isLoggedIn==False):
                system("cls")
                print(Fore.RED+'Lütfen Önce Giriş Yapınız'+Style.RESET_ALL)
            elif(self.isLoggedIn and self.isGetFollowers==False):
                system("cls")
                print(Fore.GREEN+'Lütfen Önce Takipçi Listesini Alınız.!'+Style.RESET_ALL)
            else:
                system("cls")
                print(Fore.GREEN+'Bu Listeyi Çoktan Aldınız'+Style.RESET_ALL)
        
    def getfollowing(self):
        if(self.isLoggedIn and self.isGetFollowing==False):
            self.driver.get(self.url+self.username+"/following")
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

            liste = self.driver.find_element(By.CLASS_NAME,'_aano').find_elements(By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")
            takipEdlnSayisi = 0
            for i in liste:
                self.following_info.append({
                    'name':i.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'span').text,
                    'url':i.find_element(By.CLASS_NAME, "x1rg5ohu").find_element(By.TAG_NAME, 'a').get_attribute('href')
                    })
                takipEdlnSayisi += 1
            self.isGetFollowing=True
            system("cls")
            print(Fore.GREEN+'İşlem Tamamlandı'+Style.RESET_ALL)

        else:
            if(self.isLoggedIn==False):
                system("cls")
                print(Fore.RED+'Lütfen Önce Giriş Yapınız'+Style.RESET_ALL)
            elif(self.isLoggedIn and self.isGetFollowing==False):
                system("cls")
                print(Fore.RED+'Lütfen Önce Takip Edilen Kullanıcı Listesini Alınız.!'+Style.RESET_ALL)
            else:
                system("cls")
                print(Fore.GREEN+'Bu Listeyi Çoktan Aldınız'+Style.RESET_ALL)
        
    def find_unfollowers(self):
        if(self.isLoggedIn==True and self.isGetFollowers==True and self.isGetFollowing==True):
            self.unfollowers_info = [user for user in self.following_info if user not in self.followers_info]
            self.unfollowers_info_1 = [user for user in self.following_info if user not in self.followers_info]
            system("cls")
            print(Fore.CYAN+'\nGeri Takip Etmeyen Kullanıcılar'.center(10, '*')+Style.RESET_ALL)
            index =1
            for user in self.unfollowers_info:
                print(f"{index}-) {user['name']}")
                index+=1
            self.isGetUnfollowers=True
            print(Fore.GREEN+f'Geri Takip Etmeyen Kullanıcı Sayısı : {len(self.unfollowers_info)}'+Style.RESET_ALL)
        elif(self.isGetFollowers and self.isGetFollowing==False):
            system("cls")
            print(Fore.RED+'Önce Takip Edilen Kullanıcıların Listesini Almanız Gerekiyor!'+Style.RESET_ALL)
        elif(self.isGetFollowing and self.isGetFollowers==False):
            system("cls")
            print(Fore.RED+'Önce Takipçi Listesini Almanız Gerekiyor!'+Style.RESET_ALL)
        elif(self.isLoggedIn==False):
            system("cls")
            print(Fore.RED+'Önce Giriş Yapmanız Gerekiyor!'+Style.RESET_ALL)
        else:
            system("cls") 
            print(Fore.RED+'Önce Takipçi ve Takip Edilen Listelerini Almanız Gerekiyor'+Style.RESET_ALL)
    def unfollow(self):
        if self.isGetUnfollowers:
            exit_program = False
            for user in self.unfollowers_info:
                while True:
                    secim = int(input(Fore.MAGENTA+f"İsim: {user['name']} kullanıcısını takipten çıkmak istiyor musunuz?"+Style.RESET_ALL+"\n1-) Evet\n2-) Hayır\n3) Çıkış\nSecim: "))   
                    if secim == 1:
                        self.driver.get(user['url'])
                        time.sleep(3)
                        self.driver.find_element(By.XPATH, "//button[@type='button']").click()
                        time.sleep(2)
                        self.driver.find_element(By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 xw2csxc x1odjw0f x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div[8]/div[1]").click()
                        del self.following_info[self.following_info.index({'name': user['name'], 'url': user['url']})]
                        del self.unfollowers_info[self.unfollowers_info.index({'name': user['name'], 'url': user['url']})]
                        del self.unfollowers_info_1[self.unfollowers_info.index({'name': user['name'], 'url': user['url']})]
                        break
                    elif secim == 2:
                        del self.unfollowers_info_1[self.unfollowers_info.index({'name': user['name'], 'url': user['url']})]
                        break 
                    elif secim == 3:
                        exit_program = True
                        break 
                    else:
                        print(Fore.RED+"Geçersiz seçim. Lütfen tekrar deneyin."+Style.RESET_ALL)

                if exit_program:
                    break  
                        

                     
        else:
            system("cls")
            print(Fore.RED+"Lütfen Önce Unfollow Listesini Göster Butonuna Basınız"+Style.RESET_ALL)
    def unfollow_1(self):
        if self.isGetUnfollowers:
            exit_program = False
            for user in self.unfollowers_info_1:
                while True:
                    secim = int(input(Fore.MAGENTA+f"İsim: {user['name']} kullanıcısını takipten çıkmak istiyor musunuz?"+Style.RESET_ALL+"\n1-) Evet\n2-) Hayır\n3) Çıkış\nSecim: "))   
                    if secim == 1:
                        self.driver.get(user['url'])
                        time.sleep(3)
                        self.driver.find_element(By.XPATH, "//button[@type='button']").click()
                        time.sleep(2)
                        self.driver.find_element(By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 xw2csxc x1odjw0f x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div[8]/div[1]").click()
                        del self.following_info[self.following_info.index({'name': user['name'], 'url': user['url']})]
                        del self.unfollowers_info[self.unfollowers_info.index({'name': user['name'], 'url': user['url']})]
                        del self.unfollowers_info_1[self.unfollowers_info.index({'name': user['name'], 'url': user['url']})]
                        break
                    elif secim == 2:
                        del self.unfollowers_info_1[self.unfollowers_info.index({'name': user['name'], 'url': user['url']})]
                        break 
                    elif secim == 3:
                        exit_program = True
                        break 
                    else:
                        print(Fore.RED+"Geçersiz seçim. Lütfen tekrar deneyin."+Style.RESET_ALL)

                if exit_program:
                    break  


                     
        else:
            system("cls")
            print(Fore.RED+"Lütfen Önce Unfollow Listesini Göster Butonuna Basınız"+Style.RESET_ALL)
    
    def unfollowMulti(self):
        if self.isGetUnfollowers:
            self.find_unfollowers()
            print(Fore.CYAN+"\nSayıların arasına virgül koyunuz örnek(1,32,28,30,12)"+Style.RESET_ALL)
            sayi_listesi = [int(sayi)-1 for sayi in input("Hangi indexli kullanıcıları takipten çıkmak istiyorsunuz: ").split(",")]
            for i in sayi_listesi:
                self.driver.get(self.unfollowers_info[i]['url'])
                time.sleep(3)
                self.driver.find_element(By.XPATH,"//button[@type='button']").click()
                time.sleep(2)
                self.driver.find_element(By.XPATH,"//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 xw2csxc x1odjw0f x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div[8]/div[1]").click()
                time.sleep(2)
                del self.following_info[self.following_info.index({'name': self.unfollowers_info[i]['name'], 'url':self.unfollowers_info[i]['url']})]

            self.unfollowers_info = [eleman for indeks, eleman in enumerate(self.unfollowers_info) if indeks not in sayi_listesi]
            



        else:
            system("cls")
            print(Fore.RED+"Lütfen Önce Unfollow Listesini Göster Butonuna Basınız"+Style.RESET_ALL)        

    def display_followers(self):
        if(self.isGetFollowers):
            print(Fore.CYAN+'\nSizi Takip Edenlerin Listesi :'+Style.RESET_ALL)
            for user in self.followers_info:
                print(f"İsim : {user['name']}")
            print(Fore.CYAN+f'Toplam Takipçi Sayınız : {len(self.followers_info)}'+Style.RESET_ALL)
        else:
            system("cls")
            print(Fore.RED+'\nLütfen Önce Takipçi Listesini AL seçeneğine Tıklayınız'+Style.RESET_ALL)
    def display_following(self):
        if(self.isGetFollowing):
            print(Fore.CYAN+'\nTakip Edilen Listesi :'+Style.RESET_ALL)
            for user in self.following_info:
                print(f"İsim : {user['name']}")
            print(f'Sizi Takip Eden Kullanıcı Sayısı : {len(self.following_info)}')
        else:
            system("cls")
            print(Fore.RED+'\nLütfen Önce Takip Edilen Listesini Al Seçeneğine Tıklayınız'+Style.RESET_ALL)
    def Menu(self):
        while True:
            if(self.isLoggedIn):
                print(Fore.GREEN+'\nİnstagrama Giriş Yapıldı '+Style.RESET_ALL)
            else:
                print(Fore.RED+'\nGiriş Yapılmadı '+Style.RESET_ALL) 
            print(Fore.CYAN+"İnstagram App Menu".center(20,'*')+Style.RESET_ALL)
            secim=int(input(f"1) İnstagrama Giriş Yap\n2) Takip Edilen Kullanıcıları İşlemleri\n3) Takipçi Sayısını Göster\n4) Geri Takip Etmeyen Kullanıcıları Kontrol Et\n5) Çıkış\nSeçim : "))
            if secim==1:
                system("cls")
                self.signIn()
            if secim==2:
                system("cls") 
                while True:
                    print(Fore.CYAN+'\nTakip Edilen Kullanıcılar İşlemleri'.center(10,'*')+Style.RESET_ALL)
                    takip_secim=int(input('1) Takip Edilen Kullanıcıların Listesini Al\n2) Takip Edilen Kullanıcıların Listesini Ve Sayısını Göster\n3) Giriş Yap \n4) Ana Menu\n5) Çıkış\nSeçim : '))
                    if(takip_secim==1):
                        self.getfollowing()
                    if(takip_secim==2):
                        self.display_following()
                    if(takip_secim==3):
                        self.signIn()
                    if(takip_secim==4):
                        break
                    if(takip_secim==5):
                        exit()
            if secim==3:
                system("cls")
                while True:
                    print(Fore.CYAN+'\nTakipçi İşlemleri'.center(10,'*')+Style.RESET_ALL)
                    takip_secim=int(input('1) Takipçi Listesini Al\n2) Takipçi Listesini Ve Sayısını Göster\n3) Giriş Yap\n4) Ana Menu\n5) Çıkış\nSeçim : '))
                    if(takip_secim==1):
                        self.getFollowers()
                    if(takip_secim==2):
                        self.display_followers()
                    if(takip_secim==3):
                        self.signIn()
                    if(takip_secim==4):
                        break
                    if(takip_secim==5):
                        exit()
            if secim==4:
                system("cls")
                while True:
                    print(Fore.CYAN+'\nUnfollower İşlemleri'.center(10,'*')+Style.RESET_ALL)
                    unf_secim=int(input('1) Unfollower Listesini Göster\n2) Takipten Çık (Bütün Kullanıcılar Tek Tek Sorulur) \n3) Belirtilen Kullanıcıları Takipten Çık\n4) Takipçi Listesini Al\n5) Takip Edilen Kullanıcıların Listesini Al\n6) Giriş Yap\n7) Ana Menu\n8) Çıkış\nSeçim : '))
                    if(unf_secim==1):
                        self.find_unfollowers()
                    if(unf_secim==2):
                        while True:
                            system("cls")
                            unf_secim_1=int(input('1) Bütün Takip Etmeyenleri Tek Tek Sor :(\n2) Kaldığın Yerden Devam Et\n'+Fore.YELLOW+"Seçiminiz :"+Style.RESET_ALL))
                            if(unf_secim_1 == 1):
                                if(self.isGetFollowers==True and self.isGetFollowing== True):
                                    self.unfollow()
                                else:
                                    print('Eksik Bilgileri Tamamlayın')
                            if(unf_secim_1 == 2):
                                if(self.isGetFollowers==True and self.isGetFollowing== True):
                                    self.unfollow_1()
                                else:
                                    print('Eksik Bilgileri Tamamlayın')

                            else:
                                break
                        
                    if(unf_secim==3):
                        self.unfollowMulti()
                    if(unf_secim==4):
                        self.getFollowers()
                    if(unf_secim==5):
                        self.getfollowing()
                    if(unf_secim==6):
                        self.signIn()
                    if(unf_secim==7):
                        break
                    if(unf_secim==8):
                        exit()


k1 = Instagram()
k1.Menu()

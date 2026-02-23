from requests import Session

class AuthorToday:
    def __init__(self) -> None:
        self.api = "https://api.author.today"
        self.web_api = "https://author.today"
        self.token = "Bearer guest"
        self.session = Session()
        self.session.headers = {
            "Authorization": self.token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
    
    def login(
            self,
            login: str,
            password: str) -> dict:
        data = {
            "login": login,
            "password": password
        }
        response = self.session.post(
            f"{self.api}/v1/account/login-by-password",
            json=data).json()
        if "token" in response:
            self.token = response["token"]
            self.session.headers["Authorization"] = f"Bearer {self.token}"
            self.user_id = self.get_account_info()["id"]
        return response 
    
    def login_with_token(self, token: str) -> dict:
        self.token = token
        self.session.headers["Authorization"] = f"Bearer {self.token}"
        response = self.get_account_info()
        self.user_id = response["id"] if "id" in response else None
        return response

    def get_account_info(self) -> dict:
        return self.session.get(
            f"{self.api}/v1/account/current-user").json()
    
    def register(
            self,
            nickname: str,
            email: str,
            password: str) -> dict:
        data = {
            "email": email,
            "fio": nickname,
            "password": password,
            "termsAgree": True
        }
        return self.session.post(
            f"{self.api}/v1/account/register",
            json=data).json()

    def refresh_token(self) -> dict:
        return self.session.post(
            f"{self.api}/v1/account/refresh-token").json()

    def recover_password(self, email: str) -> dict:
        data = {
            "email": email
        }
        return self.session.post(
            f"{self.api}/v1/account/password/recovery").json()

    def check_notifications(self) -> dict:
        return self.session.get(
            f"{self.web_api}/notification/check").json()

    def get_work_content(self, work_id: int) -> dict:
        return self.session.get(
            f"{self.api}/v1/work/{work_id}/content").json()

    def get_work_meta_info(self, work_id: int) -> dict:
        return self.session.get(
            f"{self.api}/v1/work/{work_id}/meta-info").json()
    
    def edit_profile(
            self,
            username: str = None,
            nickname: str = None,
            status: str = None,
            birthday_day: int = None,
            birthday_month: int = None,
            birthday_year: int = None,
            sex: int = -1) -> dict:
        data = {}
        if username:
            data["UserName"] = username
        if nickname:
            data["FIO"] = nickname
        if status:
            data["Status"] = status
        if birthday_day:
            data["BirthdayDay"] = birthday_day
        if birthday_month:
            data["BirthdayMonth"] = birthday_month
        if birthday_year:
            data["BirthdayYear"] = birthday_year
        if sex:
            data["Sex"] = sex
        return self.session.post(
            f"{self.web_api}/account/main-info",
            data=data).json()

    def get_disputed_works(self) -> dict:
        return self.session.get(
            f"{self.web_api}/widget/disputedWorks").json()

    def track_last_activity(self) -> dict:
        return self.session.post(
            f"{self.web_api}/account/trackLastActivity").json()

    def add_to_library(self, id: int, state: str) -> dict:
        data = {
            "ids": [id],
            "state": state
        }
        return self.session.post(
            f"{self.web_api}/work/updateLibrary", data=data).json()

    def send_report(
            self,
            category: str,
            comment: str,
            target_id: int,
            target_type: str,
            url: str) -> dict:
        data = {
            "TargetId": target_id,
            "targetType": target_type,
            "Category": category,
            "Comment": comment,
            "Url": url
        }
        return self.session.post(
            f"{self.api}/v1/feedback/complaint",
            json=data).json()

    def search(self, title: str) -> dict:
        return self.session.get(
            f"{self.web_api}/search?q={title}").json()

    def get_chapter(
            self,
            work_id: int,
            chapter_id: int) -> dict:
        return self.session.get(
            f"{self.web_api}/reader/{work_id}/chapter?id={chapter_id}").json()

    def send_message(
            self,
            message: str,
            chat_id: int) -> dict:
        data = {
            "chatId": chat_id,
            "text": f"<p>{message}<p>"
        }
        return self.session.post(
            f"{self.web_api}/pm/sendMessage",
            data=data).json()

    def mark_as_read(self, chat_id: int) -> dict:
        data = {
            "chatId": chat_id
        }
        return self.session.post(
            f"{self.web_api}/pm/markAsRead", data=data).json()

    def get_chat_messages(self, chat_id: int) -> dict:
        return self.session.get(
            f"{self.web_api}/pm/messages?id={chat_id}").json()

    def get_my_chats(self, page: int = 1) -> dict:
        return self.session.get(
            f"{self.web_api}/pm/recentChats?page={page}&onlyUnread=false").json()

    def follow_user(self, user_id: str) -> dict:
        data = {
            "subscribe": True,
            "toggleOnlyShowingUpdates": False,
            "userId": user_id
        }
        return self.session.post(
            f"{self.web_api}/subscription/updateSubscription",
            data=data).json()

    def add_user_to_ignore(self, user_id: str) -> dict:
        data = {
            "userId": user_id
        }
        return self.session.post(
            f"{self.web_api}/ignoreList/add", data=data).json()

    def like_work(
            self,
            work_id: int,
            is_liked: bool = True) -> dict:
        return self.session.post(
            f"{self.api}/v1/work/{work_id}/like?isLiked={is_liked}").json()

    def get_account_library(self) -> dict:
        return self.session.get(
            f"{self.api}/v1/account/user-library").json()

    def get_catalog(
            self,
            sorting: str,
            page: int = 1,
            ps: int = 40,
            genre: str = "all",
            form: str = "any",
            state: str = "any",
            series: str = "any",
            access: str = "any",
            dnl: str = "any",
            promo: str = "hide",
            upd: int = -1,
            pub: int = -1,
            length: str = "any",
            fnd: bool = False,
            rec: bool = False,
            exc: bool = False,
            disc: bool = False) -> dict:
        return self.session.get(
            f"{self.api}/v1/catalog/search?page={page}&ps={ps}&genre={genre}&sorting={sorting}&form={form}&state={state}&series={series}&access={access}&dnl={dnl}&promo={promo}&upd={upd}&pub={pub}&length={length}&fnd={fnd}&rec={rec}&exc={exc}&disc={disc}").json()

    def get_home_page(self, view: str = "all") -> dict:
        return self.session.get(
            f"{self.api}/v1/home/home-page?View={view}").json()

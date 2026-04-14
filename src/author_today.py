from requests import Session
from re import search, DOTALL

class AuthorToday:
	def __init__(self) -> None:
		self.api = "https://api.author.today"
		self.web_api = "https://author.today"
		self.token = "Bearer guest"
		self.session = Session()
		self.session.headers = {
			"Authorization": self.token,
			"User-Agent": "Mozilla/5.0 (Linux; Android 9; 2203121C Build/PQ3A.190705.09121607; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Mobile Safari/537.36 at-lt AuthorToday/android_1.8.026-GMS",
			"X-Requested-With": "XMLHttpRequest",
			"Content-Type": "application/json"
		}
		self.user_id = None

	def _post(self, endpoint: str, data: dict = None) -> dict:
		return self.session.post(endpoint, json=data).json()

	def _get(self, endpoint: str, params: dict = None) -> dict:
		return self.session.get(endpoint, params=params).json()

	def login(
			self,
			login: str,
			password: str) -> dict:
		data = {
			"login": login,
			"password": password
		}
		response = self._post(
			f"{self.api}/v1/account/login-by-password", data)
		if "token" in response:
			self.token = response["token"]
			self.session.headers["Authorization"] = f"Bearer {self.token}"
			self.get_login_cookie_by_token(self.token)
			self.user_id = self.get_account_info()["id"]
		return response 

	def get_login_cookie_by_token(self, token: str) -> dict:
		params = {
			"token": token
		}
		return self._get(
			f"{self.web_api}/account/login-cookie-by-token", params)

	def login_with_token(self, token: str) -> dict:
		self.token = token
		self.session.headers["Authorization"] = f"Bearer {self.token}"
		response = self.get_account_info()
		self.user_id = response["id"] if "id" in response else None
		return response

	def get_request_verification_token(self, form_url: str) -> str:
		response = self.session.get(form_url).text
		verification_token = search(
			r'<input[^>]*name="__RequestVerificationToken"[^>]*value="([^"]+)"',
			response,
			DOTALL
		).group(1)
		self.session.headers["RequestVerificationToken"] = verification_token
		return verification_token

	def get_account_info(self) -> dict:
		return self._get(f"{self.api}/v1/account/current-user")
	
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
		return self._post(f"{self.api}/v1/account/register", data)

	def refresh_token(self) -> dict:
		return self._post(f"{self.api}/v1/account/refresh-token")

	def recover_password(self, email: str) -> dict:
		data = {
			"email": email
		}
		return self._post(
			f"{self.api}/v1/account/password/recovery", data)

	def check_notifications(self) -> dict:
		return self._get(f"{self.web_api}/notification/check")

	def get_work_content(self, work_id: int) -> dict:
		return self._get(f"{self.api}/v1/work/{work_id}/content")

	def get_work_details(
			self, work_id: int, recommendations_count: int = 15) -> dict:
		params = {
			"recommendationsCount": recommendations_count
		}
		return self._get(f"{self.api}/v1/work/{work_id}/details", params)

	def get_work_meta_info(self, work_id: int) -> dict:
		return self._get(f"{self.api}/v1/work/{work_id}/meta-info")

	def edit_profile(
			self,
			username: str = None,
			fio: str = None,
			status: str = None,
			birthday_day: int = None,
			birthday_month: int = None,
			birthday_year: int = None,
			sex: int = None,
			about_me: str = None,
			privacy_show_birthday: int = 0) -> dict:
		fields = {
			"PrivacyShowBirthDay": privacy_show_birthday,
			"UserName": username,
			"FIO": fio,
			"Status": status,
			"BirthdayDay": birthday_day,
			"BirthdayMonth": birthday_month,
			"BirthdayYear": birthday_year,
			"Sex": sex,
			"AboutMe": about_me
		}
		data = {key: value for key, value in fields.items() if value is not None}
		self.get_request_verification_token(f"{self.web_api}/account/my-page")
		temporary_headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"X-Requested-With": "XMLHttpRequest",
			"Referer": f"{self.web_api}/account/my-page"
		}
		return self.session.post(
			f"{self.web_api}/account/main-info",
			data=data,
			headers=temporary_headers).json()

	def create_post(
			self,
			title: str,
			text: str,
			tags: str,
			category_id: int = 1,
			privacy_display: int = 0,
			post_editors_enabled: bool = False,
			privacy_comments: int = 0) -> dict:
		verification_token = self.get_request_verification_token(
			f"{self.web_api}/post/create")
		data = {
			"__RequestVerificationToken": verification_token,
			"Id": "",
			"CategoryId": category_id,
			"Title": title,
			"Text": text,
			"tags": tags,
			"PrivacyDisplay": privacy_display,
			"PostEditorsEnabled": post_editors_enabled,
			"PrivacyComments": privacy_comments
		}
		temporary_headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"X-Requested-With": "XMLHttpRequest",
			"Referer": f"{self.web_api}/post/create",
		}
		return self.session.post(
			f"{self.web_api}/post/edit",
			data=data,
			headers=temporary_headers).json()

	def get_disputed_works(self) -> dict:
		return self._get(f"{self.web_api}/widget/disputedWorks")

	def track_last_activity(self) -> dict:
		return self._post(
			f"{self.web_api}/account/trackLastActivity")

	def add_to_library(self, work_id: int, state: str) -> dict:
		data = {
			"ids": [work_id],
			"state": state
		}
		return self._post(f"{self.web_api}/work/updateLibrary", data)

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
		return self._post(f"{self.api}/v1/feedback/complaint", data)

	def search(self, query: str) -> dict:
		params = {
			"q": query
		}
		return self._get(f"{self.web_api}/search", params)

	def get_chapter(
			self,
			work_id: int,
			chapter_id: int) -> dict:
		params = {
			"id": chapter_id
		}
		return self._get(
			f"{self.web_api}/reader/{work_id}/chapter", params)

	def send_message(
			self,
			message: str,
			chat_id: int) -> dict:
		data = {
			"chatId": chat_id,
			"text": f"<p>{message}</p>"
		}
		return self._post(
			f"{self.web_api}/pm/sendMessage", data)

	def mark_as_read(self, chat_id: int) -> dict:
		data = {
			"chatId": chat_id
		}
		return self._post(
			f"{self.web_api}/pm/markAsRead", data)

	def get_chat_messages(self, chat_id: int) -> dict:
		params = {
			"id": chat_id
		}
		return self._get(
			f"{self.web_api}/pm/messages", params)

	def get_my_chats(
			self, page: int = 1, only_unread: bool = False) -> dict:
		params = {
			"page": page,
			"onlyUnread": only_unread
		}
		return self._get(
			f"{self.web_api}/pm/recentChats", params)

	def follow_user(self, user_id: str) -> dict:
		data = {
			"subscribe": True,
			"toggleOnlyShowingUpdates": False,
			"userId": user_id
		}
		return self._post(
			f"{self.web_api}/subscription/updateSubscription", data)

	def add_user_to_ignore(self, user_id: str) -> dict:
		data = {
			"userId": user_id
		}
		return self._post(
			f"{self.web_api}/ignoreList/add", data)

	def like_work(
			self,
			work_id: int,
			is_liked: bool = True) -> dict:
		return self._post(
			f"{self.api}/v1/work/{work_id}/like?isLiked={is_liked}")

	def get_account_library(self) -> dict:
		return self._get(f"{self.api}/v1/account/user-library")

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
		params = {
			"page": page,
			"ps": ps,
			"genre": genre,
			"sorting": sorting,
			"form": form,
			"state": state,
			"series": series,
			"access": access,
			"dnl": dnl,
			"promo": promo,
			"upd": upd,
			"pub": pub,
			"length": length,
			"fnd": fnd,
			"rec": rec,
			"exc": exc,
			"disc": disc
		}
		return self._get(
			f"{self.api}/v1/catalog/search", params)

	def get_home_page(self, view: str = "all") -> dict:
		params = {
			"View": view
		}
		return self._get(f"{self.api}/v1/home/home-page", params)

	def send_comment(
			self,
			root_id: int,
			text: str,
			root_type: str = "Work",
			is_pinned: bool = False) -> dict:
		data = {
			"rootId": root_id,
			"rootType": root_type,
			"text": text,
			"isPinned": is_pinned
		}
		if root_type == "Work":
			token_url = f"{self.web_api}/android/comments/work/{root_id}"
		elif root_type == "Post":
			token_url = f"{self.web_api}/post/{root_id}"
		elif root_type == "UserProfile":
			token_url = f"{self.web_api}/u/{root_id}"
		else:
			raise ValueError(f"Unknown root_type: {root_type}")
		self.get_request_verification_token(token_url)
		return self._post(
			f"{self.web_api}/comment/submit", data)

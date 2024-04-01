import smtplib
from email.mime.text import MIMEText
from settings import Sql_Param

class pymail:
    def __init__(self) -> None:
        self.app_password = Sql_Param.mail_passwd
        self.sender_email = Sql_Param.mail_from
        self.receiver_email = Sql_Param.mail_to

    def send_mail(self, subject, discription):
        #本文
        body = discription
        msg = MIMEText(body)
        #メールの件名
        msg["Subject"]=subject
        #あなたのGmailアドレス
        msg["From"]=self.sender_email
        #メールの送信先
        msg["To"]=self.receiver_email

        # SMTPサーバーに接続してメールを送信
        try:
            smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp_server.login(self.sender_email, self.app_password)
            smtp_server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            smtp_server.quit()
            print("Email sent successfully!")
        except smtplib.SMTPAuthenticationError as e:
            print("SMTP Authentication Error:", e)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == '__main__':
    ins = pymail()
    ins.send_mail('test','test body \n hello world...')
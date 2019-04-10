import smtplib

smtpObj = smtplib.SMTP('smtp.yandex.ru', 587)
smtpObj.ehlo()
smtpObj.starttls()

to = "tetropentada@mail.ru"
from_ = "mark.2406@yandex.ru"

smtpObj.login(from_, 'Mark.240607777777sssssss')
msg = "\r\n".join((
    "From: %s" % from_,
    "To: %s" % to,
    "Subject: %s" % "dadada",
    "",
    "Go to bed"
))
smtpObj.sendmail(from_, to, msg)
smtpObj.quit()

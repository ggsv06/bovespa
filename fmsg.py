import smtplib
import email.message

def enviar_email(key, mail, taxa):  
    corpo_email = f"""
    <p>A taxa de {taxa}% foi atingida!</p>
    <p>Obrigado por utilizar este software de Gian Gabriel</p>
    """
# Tag 'yjtlexulptslkbrn'
    msg = email.message.Message()
    msg['Subject'] = "ALERTA! A TAXA FOI ATINGIDA"
    msg['From'] = mail
    msg['To'] = mail
    password = key 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
if __name__ == '__main__':
    enviar_email()
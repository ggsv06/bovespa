import smtplib
import email.message

def enviar_email(key, remetente, destinatario, taxa, nome1, nome2):  
    corpo_email = f"""
    <p>A meta de {taxa:.2%} foi atingida!</p>
    <p>{nome1.upper()} e {nome2.upper()}</p>
    <p></p>
    <p>Obrigado por utilizar este software de Gian Gabriel</p>
    """
    msg = email.message.Message()
    msg['Subject'] = "🚨 ALERTA! A META FOI ATINGIDA 🚨"
    msg['From'] = remetente
    msg['To'] = destinatario
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
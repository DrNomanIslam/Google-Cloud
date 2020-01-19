from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
import codecs
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys

def email_report(sub,body):
    print("Sending an email with subject: ",sub)
    fromaddr = "noman.islam@gmail.com"
    toaddr = "noman.islam@nu.edu.pk"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = sub

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "$5$0$GL$")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def sentiment_text(text):
    """Detects sentiment in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    sentiment = client.analyze_sentiment(document).document_sentiment

    return sentiment

print("*******************************************************************************************")
print("*       Welcome to the three Prong solution to Faculty Evaluation - Sentiment Analysis    *")
print("*******************************************************************************************")

print("\nPerforming sentiment analysis")
data=""
fname=sys.argv[1]
with codecs.open(fname+'.txt', "r",encoding='utf-8', errors='ignore') as f:
	for l in f:
		data+=l
s = sentiment_text(l)
print("Results of sentiment analysis")
print("Score: ", s.score)
print("Magnitude: ", s.magnitude)

if s.score>0.5:
    email_report("Attn: Faculty Evaluation","Congratulations! The faculty "+ fname+ " has been very positively evaluated by students")
elif s.score<0:
    email_report("Attn: Faculty Evaluation", "Ah! The faculty "+ fname+ " has been very negatively evaluated by students")
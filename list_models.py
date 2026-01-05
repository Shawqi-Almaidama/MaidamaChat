from openai import OpenAI

# تأكد أنك عندك OPENAI_API_KEY في متغيرات البيئة
client = OpenAI()

models = client.models.list()
for m in models.data:
    print(m.id)

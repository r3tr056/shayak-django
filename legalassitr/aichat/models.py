from django.db import models

class DynamicForm(models.Model):
    form_id = models.CharField(max_length=255)
    form_title = models.CharField(max_length=255)
    form_data = models.JSONField()

class Role(models.TextChoices):
    USER = "USER", "user"
    ASSISTANT = "ASSIS","assistant"
    SYSTEM = "SYS", "system"

class FinishReason(models.TextChoices):
    STOP = "STOP", "stop"
    LENGTH = "LENGTH", "length"

class Message(models.Model):
    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField()

    def __str__(self):
        return f'{self.get_role_display()}: {self.content}'
    
class TextCompletion(models.Model):
    finish_reason = models.CharField(max_length=10, choices=FinishReason.choices, default=FinishReason.STOP)

class TextCompletionOption(models.Model):
    index = models.IntegerField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    finish_reason = models.CharField(max_length=10, choices=FinishReason.choices)

    def __str__(self):
        return f'Option {self.index} for {self.message} : {self.get_finish_reason_display()}'
    
class TextCompletionResponse(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=255)
    generations = models.ManyToManyField(TextCompletionOption)

    def __str__(self):
        return f"TextCompletionResponse created={self.created}, model={self.model}"
    
class TextCompletionRequest(models.Model):
    gen_model = models.CharField(max_length=255)
    messages = models.ManyToManyField(Message)
    stream = models.BooleanField(default=False)
    temp = models.FloatField(null=True, blank=True)
    top_p = models.FloatField(null=True, blank=True)
    n = models.IntegerField(default=1)
    max_new_tokens = models.IntegerField(null=True, blank=True)
    repetition_penalty = models.FloatField(default=1.0)

    def __str__(self):
        return f'TextCompletionRequest model={self.model} stream={self.stream}, n={self.n}'
    
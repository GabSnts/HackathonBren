from django.db import models

class Conversation(models.Model):
    last_message_ai = models.CharField(max_length=100)
    last_message_human = models.CharField(max_length=100)
    
    class Meta:
        db_table = "message"
        verbose_name = "message"
        verbose_name_plural = "messages"

    def __str__(self):     
        return f"{self.last_message_ai}-{self.last_message_human}"
from django.db import models

class Question(models.Model):
	text = models.CharField("Question", max_length=500)
	votes = models.IntegerField(default=0)
	status = models.CharField("Status", max_length=10,
							  choices=(('new','new',),
									   ('current','current',),
									   ('archived','archived',))
							 )
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.text
	
	def increment_votes(self, int):
		self.votes += int
		self.save()
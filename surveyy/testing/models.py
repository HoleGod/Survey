from django.db import models
from django.contrib.auth.models import User

SINGLE = "single"
MULTIPLE = "multiple"

QUESTION_TYPES = [
	(SINGLE, "Single choice"),
	(MULTIPLE, "Multiple choice"),
]

class Test(models.Model):
	title = models.CharField(max_length=300)
	image = models.ImageField(upload_to="banners/", blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tests")
	
	def get_points(self):
		total = 0
		for q in self.questions.all():
			total += q.points
		return total
	
class Question(models.Model):
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
	text = models.CharField(max_length=400)
	points = models.IntegerField(default=1)
	image = models.ImageField(upload_to="questions/", blank=True, null=True)
	question_type = models.CharField(
		max_length=40,
		choices=QUESTION_TYPES,
		default=SINGLE,
	)
	
class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
	text = models.CharField(max_length=150)
	is_correct = models.BooleanField(default=False)

class UserTest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tests")
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="passes")
	
class UserAnswer(models.Model):
	user_test = models.ForeignKey(
		UserTest,
		on_delete=models.CASCADE,
		related_name="answers"
	)
	question = models.ForeignKey(
		Question,
		on_delete=models.CASCADE
	)
	selected_answers = models.ManyToManyField(Answer)
	
	class Meta:
		unique_together = ("user_test", "question")
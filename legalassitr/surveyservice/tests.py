from django.test import TestCase
from users.models import User
from .models import Feedback

class FeedbackModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@gmail.com', password='testpassword', first_name='Test', last_name='User')
        self.feedback = Feedback.objects.create(user=self.user, content='This is a test feedback', rating=5)

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.user, self.user)
        self.assertEqual(self.feedback.content, 'This is a test feedback')
        self.assertEqual(self.feedback.rating, 5)

    def test_analyze_sentiment_positive(self):
        sentiment_result = self.feedback.analyze_sentiment()
        self.assertEqual(sentiment_result, 'positive')

    def test_analyze_sentiment_negative(self):
        self.feedback.content = 'This is a negative feedback'
        self.feedback.save()
        sentiment_result = self.feedback.analyze_sentiment()
        self.assertEqual(sentiment_result, 'negative')
        

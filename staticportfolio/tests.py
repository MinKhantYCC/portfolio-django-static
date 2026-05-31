from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import OperationalError
from django.test import TestCase
from django.urls import Resolver404, resolve, reverse

from . import views
from .models import ContactMessage, Testimonial


class PortfolioViewTests(TestCase):
    def test_index_uses_json_fallback_when_database_is_empty(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Min Khant")
        self.assertContains(response, "TalkEase")
        self.assertContains(response, "How to build your AI chatbot")
        self.assertContains(response, "Contact Form")
        self.assertNotContains(response, "Testimonials")

    def test_index_hides_testimonials_when_database_is_empty(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "data-testimonials-item")

    def test_index_renders_active_testimonials_from_database(self):
        Testimonial.objects.create(
            name="Jane Reviewer",
            picture_url="https://example.com/jane.png",
            recommendation_message="A clear and reliable engineering partner.",
        )
        Testimonial.objects.create(
            name="Hidden Reviewer",
            picture_url="https://example.com/hidden.png",
            recommendation_message="This should not render.",
            is_active=False,
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testimonials")
        self.assertContains(response, "Jane Reviewer")
        self.assertContains(response, "https://example.com/jane.png")
        self.assertContains(response, "A clear and reliable engineering partner.")
        self.assertNotContains(response, "Hidden Reviewer")

    def test_contact_form_saves_message(self):
        response = self.client.post(
            reverse("home"),
            {
                "fullname": "Test Sender",
                "email": "sender@example.com",
                "message": "Hello from the test suite.",
            },
        )

        self.assertRedirects(response, f"{reverse('home')}#contact")
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.get()
        self.assertEqual(message.full_name, "Test Sender")
        self.assertEqual(message.email, "sender@example.com")

    def test_letter_to_thon_url_is_removed(self):
        with self.assertRaises(Resolver404):
            resolve("/letter-to-thon")

    def test_index_uses_json_fallback_when_database_is_unavailable(self):
        with patch.object(views.Profile.objects, "filter", side_effect=OperationalError):
            response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Min Khant")


class EnsureAdminCommandTests(TestCase):
    def test_ensure_admin_creates_superadmin_from_environment(self):
        output = StringIO()
        with patch.dict(
            "os.environ",
            {
                "ADMIN_USERNAME": "admin",
                "ADMIN_PASSWORD": "strong-test-password",
            },
        ):
            call_command("ensure_admin", stdout=output)

        User = get_user_model()
        user = User.objects.get(username="admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("strong-test-password"))
        self.assertNotIn("strong-test-password", output.getvalue())

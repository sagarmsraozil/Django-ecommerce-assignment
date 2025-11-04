from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model # IMPORT THIS
from .models import Item, Order, OrderItem

# Get the standard User model
# We need to do this because the project uses a custom UserProfile,
# but the auth system still uses the base User.
User = get_user_model() # FIX THIS LINE

class CoreModelTests(TestCase):

    def setUp(self):
        # This runs before each test
        self.item = Item.objects.create(
            title="Test Item",
            price=100.00,
            category='S', # 'S' for 'Shirt'
            slug='test-item'
        )

    def test_item_creation(self):
        """Test that the Item model can be created"""
        self.assertEqual(self.item.title, "Test Item")
        self.assertEqual(self.item.price, 100.00)
        self.assertEqual(Item.objects.count(), 1)

    def test_item_str_method(self):
        """Test the string representation of the Item"""
        self.assertEqual(str(self.item), "Test Item")


class CoreViewTests(TestCase):

    def setUp(self):
        # This runs before each test
        
        # 1. Create a User
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

        # 2. Create an Item to add to the cart
        self.item = Item.objects.create(
            title="Test Book",
            price=50.00,
            category='SW', # 'SW' for 'Sport wear'
            slug='test-book'
        )

        # 3. Define the URLs we will be testing
        self.add_to_cart_url = reverse('core:add-to-cart', kwargs={'slug': self.item.slug})
        self.checkout_url = reverse('core:checkout')
        self.login_url = reverse('account_login') # From allauth

    def test_checkout_view_unauthenticated(self):
        """
        Test that an unauthenticated user is redirected
        from the checkout page to the login page.
        """
        # Make a GET request to the checkout URL without logging in
        response = self.client.get(self.checkout_url)

        # We expect a redirect (302)
        self.assertEqual(response.status_code, 302)
        
        # We expect the redirect to go to the login page
        # The '?next=/checkout/' part confirms it's redirecting correctly
        expected_redirect_url = f"{self.login_url}?next={self.checkout_url}"
        self.assertRedirects(response, expected_redirect_url)

    def test_checkout_view_authenticated(self):
        """
        Test that an authenticated user can successfully
        access the checkout page.
        """
        # Log the user in
        self.client.login(username='testuser', password='testpassword123')

        # Make a GET request
        response = self.client.get(self.checkout_url)

        # We expect a success (200)
        self.assertEqual(response.status_code, 200)
        
        # We can also check that it uses the correct template
        self.assertTemplateUsed(response, 'checkout.html')

    def test_add_to_cart_authenticated(self):
        """
        Test that an authenticated user can add an item to the cart.
        This is the most critical logic test.
        """
        # Log the user in
        self.client.login(username='testuser', password='testpassword123')

        # Check that no Order or OrderItem exists yet
        self.assertFalse(Order.objects.filter(user=self.user, ordered=False).exists())
        self.assertFalse(OrderItem.objects.filter(user=self.user, item=self.item).exists())

        # Make the GET request to the 'add-to-cart' URL
        response = self.client.get(self.add_to_cart_url)

        # It should redirect the user (e.g., back to the product page or cart)
        self.assertEqual(response.status_code, 302)

        # Now, check the database:
        # 1. An OrderItem should have been created
        self.assertTrue(OrderItem.objects.filter(user=self.user, item=self.item).exists())
        
        # 2. An active Order (ordered=False) should exist for the user
        self.assertTrue(Order.objects.filter(user=self.user, ordered=False).exists())

        # 3. Check that the order contains the item
        order = Order.objects.get(user=self.user, ordered=False)
        self.assertTrue(order.items.filter(item__slug=self.item.slug).exists())
        
    def test_add_to_cart_unauthenticated(self):
        """
        Test that an unauthenticated user cannot add to cart
        and is redirected to the login page.
        """
        # Make the GET request without logging in
        response = self.client.get(self.add_to_cart_url)
        
        # We expect a redirect (302) to the login page
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.add_to_cart_url}"
        self.assertRedirects(response, expected_redirect_url)

        # CRITICAL: Check that no Order or OrderItem was created
        self.assertFalse(Order.objects.filter(user=self.user).exists())
        self.assertFalse(OrderItem.objects.filter(user=self.user).exists())


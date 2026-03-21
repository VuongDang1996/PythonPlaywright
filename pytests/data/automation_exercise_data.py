from dataclasses import dataclass
from typing import Dict

from pytests.data.credentials import (
    get_existing_user_credentials,
    get_invalid_user_credentials,
    get_valid_user_credentials,
)


@dataclass(frozen=True)
class UserRegistrationData:
    name: str
    email: str
    title: str
    password: str
    day: str
    month: str
    year: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    country: str
    state: str
    city: str
    zipcode: str
    mobile_number: str


def build_sample_registration_data() -> Dict[str, str]:
    return {
        "name": "Test User",
        "email": "",
        "title": "Mr",
        "password": "password123",
        "day": "15",
        "month": "January",
        "year": "1990",
        "first_name": "Test",
        "last_name": "User",
        "company": "Test Company",
        "address1": "123 Test Street",
        "address2": "Apt 456",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90210",
        "mobile_number": "+1234567890",
    }


AUTOMATION_EXERCISE_TEST_DATA = {
    "epic": "Automation Exercise E2E Testing",
    "features": {
        "authentication": "User Authentication",
        "checkout": "Checkout Process",
        "contact_us": "Contact Us",
        "navigation": "Navigation & UI",
        "shopping_cart": "Shopping Cart",
        "product_catalog": "Product Catalog",
        "newsletter": "Newsletter & Subscription",
        "user_management": "User Management",
    },
    "stories": {
        "cart_management": "Cart Management",
        "contact_form": "Contact Form",
        "login": "User Login",
        "logout": "User Logout",
        "order_placement": "Order Placement",
        "page_navigation": "Page Navigation",
        "product_browsing": "Product Browsing",
        "product_search": "Product Search",
        "registration": "User Registration",
        "reviews": "Product Reviews",
        "subscription": "Newsletter Subscription",
    },
}


_valid_user = get_valid_user_credentials()
_invalid_user = get_invalid_user_credentials()
_existing_user = get_existing_user_credentials()

TEST_USERS = {
    "valid_user": {
        "email": _valid_user.email,
        "password": _valid_user.password,
    },
    "invalid_user": {
        "email": _invalid_user.email,
        "password": _invalid_user.password,
    },
    "existing_user": {
        "email": _existing_user.email,
        "password": _existing_user.password,
    },
}


SAMPLE_CONTACT_DATA = {
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Subject",
    "message": "This is a test message for the contact form. Testing automation.",
}


SAMPLE_PAYMENT_DATA = {
    "name_on_card": "Test User",
    "card_number": "4111111111111111",
    "cvc": "123",
    "expiration_month": "12",
    "expiration_year": "2025",
}


SAMPLE_REVIEW_DATA = {
    "name": "Test Reviewer",
    "email": "reviewer@example.com",
    "review": "This is an excellent product! Highly recommended for anyone looking for quality.",
}


SEARCH_TERMS = {
    "shirt": "shirt",
    "dress": "dress",
    "jeans": "jeans",
    "top": "top",
}


CATEGORIES = {
    "women": {
        "dress": "Dress",
        "tops": "Tops",
        "saree": "Saree",
    },
    "men": {
        "tshirts": "Tshirts",
        "jeans": "Jeans",
    },
}


BRANDS = {
    "polo": "Polo",
    "h_and_m": "H&M",
}

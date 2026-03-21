from pytests.pages.automation_exercise_cart_page import AutomationExerciseCartPage
from pytests.pages.automation_exercise_home_page import AutomationExerciseHomePage
from pytests.pages.automation_exercise_products_page import AutomationExerciseProductsPage


class CartFlow:
    def add_product_to_cart(
        self,
        home_page: AutomationExerciseHomePage,
        products_page: AutomationExerciseProductsPage,
        product_index: int = 0,
        continue_shopping: bool = True,
    ) -> None:
        home_page.click_products()
        products_page.hover_and_add_to_cart(product_index)
        if continue_shopping:
            products_page.click_continue_shopping()

    def open_cart(self, home_page: AutomationExerciseHomePage) -> None:
        home_page.click_cart()

    def proceed_to_checkout(self, cart_page: AutomationExerciseCartPage) -> None:
        cart_page.click_proceed_to_checkout()

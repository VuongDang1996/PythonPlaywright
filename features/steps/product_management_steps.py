from behave import then, when


@when("I click on 'Test Cases' button")
def step_click_test_cases(context):
    context.home_page.click_test_cases()


@then("I should be navigated to test cases page successfully")
def step_verify_test_cases_page(context):
    context.page.wait_for_function(
        "() => window.location.href.includes('/test_cases')", timeout=10000
    )
    test_cases_title = context.page.locator('h2:has-text("Test Cases")')
    assert test_cases_title.is_visible(), "Test Cases title is not visible"


@when("I click on 'Products' button")
def step_click_products(context):
    context.home_page.click_products()


@then("I should be navigated to ALL PRODUCTS page successfully")
def step_verify_all_products_page(context):
    context.page.wait_for_url("**/products", timeout=10000)
    assert context.products_page.all_products_title.is_visible(), "All Products title is not visible"


@then("I should see the products list is visible")
def step_verify_products_list_visible(context):
    assert context.products_page.products_list.is_visible(), "Products list is not visible"


@when("I click on 'View Product' of first product")
def step_click_first_view_product(context):
    context.products_page.click_view_product(0)


@then("I should be landed on product detail page")
def step_verify_product_detail_page(context):
    context.page.wait_for_url("**/product_details/**", timeout=10000)
    assert context.product_detail_page.product_name.is_visible(), "Product name is not visible"


@then("I should see product name, category, price, availability, condition, brand")
def step_verify_product_detail_fields(context):
    assert context.product_detail_page.product_name.is_visible(), "Product name is not visible"
    assert context.product_detail_page.product_category.is_visible(), "Product category is not visible"
    assert context.product_detail_page.product_price.is_visible(), "Product price is not visible"
    assert context.product_detail_page.product_availability.is_visible(), (
        "Product availability is not visible"
    )
    assert context.product_detail_page.product_condition.is_visible(), "Product condition is not visible"
    assert context.product_detail_page.product_brand.is_visible(), "Product brand is not visible"


@when('I enter product name "{product_name}" in search input')
def step_enter_product_name_in_search(context, product_name):
    context.search_product_name = product_name
    context.products_page.search_input.fill(product_name)


@when("I click search button")
def step_click_search_button(context):
    context.products_page.search_button.click()


@then("I should see 'SEARCHED PRODUCTS' is visible")
def step_verify_searched_products_visible(context):
    assert context.products_page.searched_products_title.is_visible(), (
        "Searched Products title is not visible"
    )


@then("I should see all the products related to search are visible")
def step_verify_search_results_visible(context):
    results_count = context.products_page.get_search_results_count()
    assert results_count > 0, "No search results are displayed"

    for index in range(results_count):
        assert context.products_page.search_results.nth(index).is_visible(), (
            f"Search result at index {index} is not visible"
        )

    search_term = getattr(context, "search_product_name", "").strip().lower()
    if search_term:
        names = context.page.locator(".features_items .productinfo p")
        matching_names = 0
        for index in range(names.count()):
            product_name = names.nth(index).inner_text().strip().lower()
            if search_term in product_name:
                matching_names += 1
        assert matching_names > 0, (
            f"No visible product names matched search term '{search_term}'"
        )


@when("I hover over first product and click 'Add to cart'")
def step_add_first_product_to_cart(context):
    context.products_page.hover_and_add_to_cart(0)


@when("I click 'Continue Shopping' button")
def step_click_continue_shopping(context):
    context.products_page.click_continue_shopping()


@when("I hover over second product and click 'Add to cart'")
def step_add_second_product_to_cart(context):
    context.products_page.hover_and_add_to_cart(1)


@when("I click 'View Cart' button")
def step_click_view_cart(context):
    context.products_page.click_view_cart()


@then("I should see both products are added to Cart")
def step_verify_two_products_in_cart(context):
    assert context.cart_page.cart_table.is_visible(), "Cart table is not visible"
    cart_items = context.cart_page.get_cart_items_count()
    assert cart_items == 2, f"Expected 2 products in cart, but found {cart_items}"


@then("I should see their prices, quantity and total price")
def step_verify_cart_price_quantity_total(context):
    prices = context.cart_page.get_product_prices()
    quantities = context.cart_page.get_product_quantities()
    totals = context.cart_page.get_product_totals()

    assert len(prices) == 2, f"Expected 2 prices, but found {len(prices)}"
    assert len(quantities) == 2, f"Expected 2 quantities, but found {len(quantities)}"
    assert len(totals) == 2, f"Expected 2 totals, but found {len(totals)}"
    assert quantities[0] == 1 and quantities[1] == 1, (
        f"Expected quantities [1, 1], but found {quantities}"
    )

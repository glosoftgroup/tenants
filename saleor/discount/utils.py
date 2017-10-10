def get_product_variants_and_prices(cart, product):
    lines = (cart_line for cart_line in cart.lines.all()
             if cart_line.variant.product_id == product.id)
    for line in lines:
        for dummy_i in range(line.quantity):
            yield line.variant, line.get_price_per_item()


def get_category_variants_and_prices(cart, discounted_category):
    products = {cart_line.variant.product for cart_line in cart.lines.all()}
    discounted_products = set()
    for product in products:
        for category in product.categories.all():
            is_descendant = category.is_descendant_of(
                discounted_category, include_self=True)
            if is_descendant:
                discounted_products.add(product)
    for product in discounted_products:
        for line in get_product_variants_and_prices(cart, product):
            yield line


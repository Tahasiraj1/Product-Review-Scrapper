from playwright.async_api import async_playwright
import asyncio

async def scrape_reviews(url, num_reviews_to_extract: int):
    reviews_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to the product page
            await page.goto(url, wait_until="networkidle", timeout=40000)
            print(f"Navigated to {url}")

            # Wait for product title
            try:
                await page.wait_for_selector("h1.pdp-mod-product-badge-title", timeout=10000)
                product_name = await page.text_content("h1.pdp-mod-product-badge-title")
                product_name = product_name.strip() if product_name else "N/A"
            except Exception as e:
                product_name = "N/A - Product Name Not Found"
                print(f"Warning: Product name element not found: {e}")

            # Scroll to ensure reviews section is loaded
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)

            while len(reviews_data) < num_reviews_to_extract:
                # Extract reviews from the current page
                review_elements = await page.locator('div.mod-reviews div.item').all()
                print(f"Found {len(review_elements)} reviews on current page.")

                for i, container in enumerate(review_elements):
                    if len(reviews_data) >= num_reviews_to_extract:
                        break

                    try:
                        # Review text
                        review_content_element = container.locator('div.item-content div.content')
                        review_text = await review_content_element.text_content() if await review_content_element.count() > 0 else "N/A"
                        review_text = review_text.strip()

                        # Star rating (count star images)
                        star_count = await container.locator('div.top div.container-star img.star').count()

                        reviews_data.append({
                            'product_name': product_name,
                            'review_text': review_text,
                            'rating': star_count,
                        })
                        print(f"Collected review {len(reviews_data)}: {review_text[:50]}...")

                    except Exception as e:
                        print(f"Skipping review {i} on current page due to error: {e}")
                        continue

                # Check for the "Next" button in the reviews section
                next_button_selector = '#module_product_review button.next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next'
                try:
                    next_button = page.locator(next_button_selector)
                    button_count = await next_button.count()
                    if button_count > 1:
                        print(f"Warning: Found {button_count} Next buttons; using the first one.")
                        next_button = next_button.first()  # Use the first match if multiple are found

                    if await next_button.is_visible() and not await next_button.is_disabled():
                        print("Clicking 'Next' button to load more reviews...")
                        await next_button.click()
                        await asyncio.sleep(3)  # Wait for new page to load
                        await page.wait_for_selector('div.mod-reviews div.item', timeout=10000)  # Ensure reviews load
                    else:
                        print("No more pages to load (Next button not visible or disabled).")
                        break
                except Exception as e:
                    print(f"Failed to interact with Next button: {e}")
                    break

                # Scroll again to ensure new reviews are in view
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)

            print(f"Total reviews collected: {len(reviews_data)}")

        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            await browser.close()

    return reviews_data
    
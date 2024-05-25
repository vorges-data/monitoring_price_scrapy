import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook#D[A:notebook]"]
    page_count = 1
    max_pages = 30

    def parse(self, response):
        products = response.css('div.ui-search-result__content')

        # Extrai URLs das imagens
        img_urls = response.css('img.ui-search-result-image__element::attr(data-src)').getall()
        if not img_urls:
            img_urls = response.css('img.ui-search-result-image__element::attr(src)').getall()

        for idx, product in enumerate(products):
            old_price = product.css('s.andes-money-amount')
            if old_price:
                old_price_reais = old_price.css('span.andes-money-amount__fraction::text').get()
                old_price_cents = old_price.css('span.andes-money-amount__cents::text').get()
                new_price_reais = product.css('div.ui-search-price__second-line span.andes-money-amount__fraction::text').get()
            else:
                old_price_reais = None
                old_price_cents = None
                new_price_reais = product.css('span.andes-money-amount__fraction::text').get()

            # Parcelamento
            installments = product.xpath('//div[@class="ui-search-installments-prefix"]/following-sibling::text()').get().strip()

            yield {
                "brand": product.css('h2.ui-search-item__title::text').get(),
                "old_price_reais": old_price_reais,
                "old_price_centavos": old_price_cents,
                "new_price_reais": new_price_reais,
                "reviews_rating_number": product.css('span.ui-search-reviews__rating-number::text').get(),
                "reviews_amount": product.css('span.ui-search-reviews__amount::text').get(),
                "supplier": product.css('p.ui-search-official-store-label.ui-search-item__group__element.ui-search-color--GRAY::text').get(),
                "product_url": product.css('a.ui-search-item__group__element.ui-search-link__title-card.ui-search-link::attr(href)').get(),
                "img_product_url": img_urls[idx] if idx < len(img_urls) else None,
                "installments": installments
            }

        # Paginação
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)

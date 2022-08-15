from django.shortcuts import render, redirect
import requests
import re
from bs4 import BeautifulSoup
from django.contrib.sites.shortcuts import get_current_site

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

# Create your views here.
def search(request):
    if request.method == "POST":
        searchInput = request.POST["search"]

    # Remove white spaces in search input
    search = re.sub("\s+", "+", searchInput)

    # Pointek Search Scraper
    pSearchUrl = "https://www.pointekonline.com/?s="+search+"&post_type=product"

    pointek = requests.get(url=pSearchUrl, headers=headers)
    psoup = BeautifulSoup(pointek.content, 'html.parser')

    # Pointek Product Url
    tag = psoup.find("a", class_="woocommerce-LoopProduct-link")
    attr = tag.attrs
    plink = attr['href']

    # Pointek Product Image Url
    tag2 = psoup.find("img", class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail")
    attr2 = tag2.attrs
    pimage = attr2['src']

    # Pointek Product Name
    tag3 = psoup.find("h2", class_="woocommerce-loop-product__title")
    pname = tag3.text

    # Pointek Product Price
    tag4 = psoup.find("span", class_="woocommerce-Price-amount amount")
    price = tag4.text
    priceText = price.replace(".00", "")
    priceText1 = priceText.replace("₦", "")
    ppriceText = priceText1.replace(",", "")
    pprice = int(ppriceText)

    # Jumia Search Scraper
    jSearchUrl = "https://www.jumia.com.ng/catalog/?q="+search+"&post_type=product"

    jumia = requests.get(url=jSearchUrl, headers=headers)
    jsoup = BeautifulSoup(jumia.content, 'html.parser')

    # Jumia Product Url
    tag6 = jsoup.find("a", class_="core")
    attr6 = tag6.attrs
    link = attr6['href']
    jlink = "https://www.jumia.com.ng"+link

    # Jumia Product Image Url
    tag7 = jsoup.find("img", class_="img")
    attr7 = tag7.attrs
    jimage = attr7['data-src']

    # Jumia Product Name
    tag8 = jsoup.find("h3", class_="name")
    jname = tag8.text

    # Jumia Product Price
    tag9 = jsoup.find("div", class_="prc")
    price2 = tag9.text
    priceText2 = price2.replace(",", "")
    jpriceText = priceText2.replace("₦", "")
    jpriceText2 = jpriceText.replace(" ", "")
    jprice = int(jpriceText2)

    if jprice < pprice:
        cheapestprice = jprice
        cheapestlink = jlink
        cheapestimage = jimage
        cheapestname = jname
    else:
        cheapestprice = pprice
        cheapestlink = plink
        cheapestimage = pimage
        cheapestname = pname

    return render(request, "product/search.html", {
        "plink": plink,
        "pimage": pimage,
        "pname": pname,
        "pprice": pprice,
        "jlink": jlink,
        "jimage": jimage,
        "jname": jname,
        "jprice": jprice,
        "cheapestprice": cheapestprice,
        "cheapestlink": cheapestlink,
        "cheapestimage": cheapestimage,
        "cheapestname": cheapestname,
    })
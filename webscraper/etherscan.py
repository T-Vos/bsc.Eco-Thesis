from selenium import webdriver

def webScraperPrice(ethTransaction_hash="0xbc8412594ffa7382e8306215ece5b4e041fc641b18133221925a4ac6ecf15432"):
    url = 'https://etherscan.io/tx/'+ethTransaction_hash
    browser = webdriver.Chrome()
    browser.get(url)
    estimatedTradeValue = browser.find_element_by_xpath('//*[@id="tokenpricebutton"]').get_property('value')
    currentTradingValue = browser.find_element_by_xpath('//*[@id="tokenpricebutton"]').text
    browser.quit()
    return estimatedTradeValue,currentTradingValue
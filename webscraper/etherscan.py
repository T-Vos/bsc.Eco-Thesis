from selenium import webdriver

def webScraperPrice(ethTransaction_hash="0xbc8412594ffa7382e8306215ece5b4e041fc641b18133221925a4ac6ecf15432"):
    url = 'https://etherscan.io/tx/'+ethTransaction_hash
    browser = webdriver.Chrome()
    browser.get(url)
    estimatedTradeValue = browser.find_element_by_xpath('//*[@id="tokenpricebutton"]').get_property('value')
    currentTradingValue = browser.find_element_by_xpath('//*[@id="tokenpricebutton"]').text
    browser.quit()
    return estimatedTradeValue,currentTradingValue

def webScraperTokenName(ethTransaction_hash="0xFBeef911Dc5821886e1dda71586d90eD28174B7d"):
    url = 'https://etherscan.io/token/'+ethTransaction_hash
    browser = webdriver.Chrome()
    browser.get(url)
    nftSymbol = browser.find_element_by_xpath('/html/head/meta[15]').get_property('content')
    nftName = browser.find_element_by_xpath('/html/body/div[1]/main/div[1]/div/div[1]/h1/div/span').text
    browser.quit()
    nftSymbol = nftSymbol[nftSymbol.find("(")+1:nftSymbol.find(")")]
    return nftSymbol,nftName
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import 选项
import time
from bs4 import BeautifulSoup
import random
from tqdm import tqdm
import json
from callapi import call_deepseek_api,call_kimi_api,call_qwen_api,call_photo_api
import re
import os

def mydriver():
    # 配置 Chrome 浏览器选项
    chrome_options = 选项()
    # 忽略 SSL 证书错误
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")
    # 启用无头模式
    chrome_options.add_argument("--headless")
    # 设置 Chrome WebDriver 的路径（如果需要）
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def mypinyin(text):
    from pypinyin import pinyin, Style
    if len(text)==1:
        return pinyin(text,style=Style.NORMAL)[0][0]
    else:
        s = ''
        for word in pinyin(text):
            s = s + word[0][0]。upper()
        return s

def config(term):
    with open('config.json'，'r+',encoding='utf-8') as f:
        c = json.load(f)
    try:
        if float(c[term]) == int(float(c[term])):
            return int(c[term])
        else:
            return float(c[term])
    except:
        return c[term]
    
def testword(text):
    with open('api.json'，'r+',encoding='utf-8') as f:
        api = json.load(f)
    text = ''。join(char for char in text if 0x0000 <= ord(char) <= 0xFFFF)
    driver = mydriver()
    try:
        driver.get('https://www.lingkechaci.com')
        time.sleep(random.randint(10，15))
        # 点击登录/注册按钮
        login_button = driver.find_element(By.CSS_SELECTOR， '.mobile_btn.func_login')
        driver.execute_script("arguments[0].click();", login_button)
        # 等待页面跳转或弹出登录框
        time.sleep(random.randint(10，15))
        iframe = driver.find_element(By.CSS_SELECTOR， "iframe")
        driver.switch_to。frame(iframe)
        account_login = driver.find_element(By.CSS_SELECTOR， 'li[lay-id="13"]')
        driver.execute_script("arguments[0].click();", account_login)

        # 填入密码
        time.sleep(random.randint(5，10))
        phone_input = driver.find_element(By.CSS_SELECTOR， 'input[name="phone"]')
        phone_input.send_keys(api[1]['phonenumber'])
        time.sleep(random.randint(2，5))
        password_input = driver.find_element(By.CSS_SELECTOR， 'input[name="password"]')
        password_input.send_keys(api[1]['password'])
        time.sleep(random.randint(5，10))
        login_button = driver.find_element(By.ID， 'subLogin')
        login_button.click()
        time.sleep(random.randint(15，20))
        driver.switch_to。default_content()
        #取消选择B站词汇
        try:
            checkbox = driver.find_element(By.XPATH， "/html/body/div[3]/div[2]/div[1]/form/div/div[6]")
            checkbox.click()
        except:
            pass

        time.sleep(random.randint(2，5))
        #填入文章
        text_area = driver.find_element(By.ID， "check_text")
        text_area.clear()
        text_area.send_keys(text)
        time.sleep(random.randint(2，5))
        check_button = driver.find_element(By.ID， "check_article")
        check_button.click()

        time.sleep(random.randint(30，60))
        #获取结果
        element = driver.find_element(By.ID， "check_view")
        html_content = element.get_attribute("innerHTML")
        soup = BeautifulSoup(html_content, 'html.parser')
        highlighted_words = soup.find_all('font', style=lambda value: 'background-color:orange' in value 和 'color:white' in value)
        words = []
        for word in highlighted_words:
            word = re.findall(r'<font style="background-color:orange;color:white;">(.*?)</font>'， str(word))
            words.append(word[0])

    except Exception as e:
        print(e)
        
    finally:
        # 关闭浏览器
        driver.quit()
        try:
            return words
        except:
            return []

def gethot(n):
    # 初始化 WebDriver（确保 chromedriver 在你的系统路径中）
    driver = mydriver()
    try:
        # 打开页面
        driver.get("https://s.weibo.com/top/summary?cate=entrank")  # 替换为你想要爬取的页面 URL

        # 等待页面加载完成
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME， 'tbody')))

        # 定位到 <tbody> 元素
        tbody = driver.find_element(By.TAG_NAME， 'tbody')

        # 获取 <tbody> 中的所有 <tr> 元素
        rows = tbody.find_elements(By.TAG_NAME， 'tr')

        # 遍历每一行，提取内容
        data = []
        for row in rows:
            # 获取每一行中的所有 <td> 元素
            cells = row.find_elements(By.TAG_NAME， 'td')

            # 遍历每个 <td> 元素
            cell_data = []
            for cell in cells:
                # 检查当前 <td> 是否是 .td-02 类型
                cell_class = cell.get_attribute('class')
                if 'td-02' in cell_class:
                    # 提取 <a> 标签的文本
                    links = cell.find_elements(By.TAG_NAME， 'a')
                    link_text = links[0]。text if links else ""

                    # 提取 <span> 标签的文本
                    spans = cell.find_elements(By.TAG_NAME， 'span')
                    span_text = spans[0]。text if spans else ""

                    # 将内容和数字分开存储
                    cell_data.append(link_text)
                    cell_data.append(span_text)
                elif 'td-01' in cell_class:
                    # 排行 <td> 类型直接提取文本
                    cell_data.append(cell.text)

            data.append(cell_data)

        # 返回前 n 条数据
        if n < len(data):
            return data[:n]
        else:
            return data
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return []
    finally:
        driver.quit()
        
def gethotcontent(n):
    hotsearchs = gethot(n)
    hots=[]
    print('由于kimi api请求速率的限制，每次访问后都需要等待60s')
    for hotsearch in tqdm(hotsearchs, desc="正在获取热搜信息"):
        quest="这是一个今天的娱乐热搜标题："+str(hotsearch[1])+"。请简要的描述其具体内容，50-200字。"
        retries = 0
        while retries < 3:
            try:
                hots.append({'排名':hotsearch[0]，
                             '标题':hotsearch[1]，
                             '内容':call_kimi_api(quest)，
                             '热度':hotsearch[2]
                             })
                time.sleep(60)
                break
            except openai.RateLimitError as e:
                print(f"速率限制错误: {e}。正在等待60秒后重试...")
                time.sleep(60)
                retries += 1
            except Exception as e:
                print(f"其他错误: {e}")
                retries += 1
            time.sleep(60)
    for h in hots:
        print(h)
    return hots

def getarticles(n):
    with open('articles.json'，'r+',encoding='utf-8') as f:
        articles = json.load(f)
    if len(articles)<n:
        inputarticles=articles
    else:
        inputarticles=articles[len(articles)-n:]
    return inputarticles

def judgeword(article):
    result = testword(article)
    retries = 0
    while True:
        quest = '这是一个文本：“'+article+'”。其中，以下部分触发了部分平台的敏感词：'+str(result)+'。请不要改变其他内容，将这些敏感词换个说法表述，并直接将完整文章输出给我。不要输出任何提示词，只输出文章！'
        article = call_qwen_api(quest)
        if retries>0:
            break
        result = testword(article)
        if len(result)<4:
            break
        retries = retries+1
    return article

def getnewarticle():
    #可调整参数：hots数量，toward，tag，rate，getarticles数量
    articles = getarticles(config("获取历史文章数量"))
    num = 0
    for article in articles:
        num = num + int(article['字数'])
    num = num/len(articles)
    hots = gethotcontent(config("获取热搜数量"))
    rate = config("字数偏离最大比率")
    newnum = 0
    toward = config("更新方向")
    if config("衔接上文"):
        quest = "这是今天的一些热搜："+str(hots)+"。这是我以前发布的一些文章"+str(articles)+"。我的更新方向是"+toward+"。请帮我根据以前文章主题继续写一篇文章，字数与以前相仿。以'标题:\n字数:\n内容:'的格式输出。注意标题应在20字以内。"
    else:
        quest = "这是今天的一些热搜："+str(hots)+"。这是我以前发布的一些文章"+str(articles)+"。我的更新方向是"+toward+"。请帮我再写一篇文章，字数与以前相仿，但不要与以前的文章选用相似的主题，规避以前提过的内容。以'标题:\n字数:\n内容:'的格式输出。注意标题应在20字以内。"
    retries = 0
    title = ""
    content=""
    word = 0
    print('正在获取deepseek文章')
    while (not(0<len(title)<=20 和 (1-rate)*num<int(word)<(1+rate)*num)) 和 retries < 5:
        try:
            response = call_deepseek_api(quest)
            print(response)
            # 分割文本为行
            lines = response.strip()。split('\n')
            for line in lines:
                if line.startswith("标题:"):
                    title = line.split("标题:")[1]。strip()
                elif line.startswith("字数:"):
                    word = line.split("字数:")[1]。strip()
                elif line.startswith("标题："):
                    title = line.split("标题：")[1]。strip()
                elif line.startswith("字数："):
                    word = line.split("字数：")[1]。strip()
                elif line.startswith("标题"):
                    title = line.split("标题")[1]。strip()
                elif line.startswith("字数"):
                    word = line.split("字数")[1]。strip()
                else:
                    content = content+'\n'+line
            retries += 1
        except Exception as e:
            print(f"错误: {e}")
            retries += 1
            if retries>=5:
                raise
            
    content = content.replace(' '，'')。replace('\n\n'，'\n')
    while content.startswith("\n"):
        content = content.split("\n"，1)[1]。strip()
    if content.startswith("内容:"):
        content = content.split("内容:")[1]。strip()
    elif content.startswith("内容："):
        content = content.split("内容：")[1]。strip()
    elif content.startswith("内容"):
        content = content.split("内容")[1]。strip()
    while content.startswith("\n"):
        content = content.split("\n"，1)[1]。strip()
    title = judgeword(title)
    content = judgeword(content)
    from datetime import datetime
    现在 = datetime.当前()
    title = title.replace(' '，'')
    return {'文章编号':int(articles[-1]['文章编号'])+1，
            '发布日期':now.strftime("%Y年%m月%d日")，
            "标题":title,
            "内容":content,
            "字数":word
            }

def main():
    new = getnewarticle()
    with open('articles.json'， 'r', encoding='utf-8') as file:
        data = json.load(file)
    data.append(new)
    with open('articles.json'， 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    retries = 0
    while retries<3:
        try:
            quest = '这是我的文章内容"'+new["内容"]+'"，请为我的文章输出一个封面提示词，我会将你输出的提示词直接导入文生图的ai模型（模型对于具体文字的渲染能力较差）。所以，请直接为我输出图片的提示词。'
            call_photo_api(quest,new["文章编号"])
        except:
            print("获取封面失败，将等待60s重试")
        finally:
            retries = retries + 1
            if os.path。exists('photo\\'+str(new["文章编号"])+'.png'):
                break
            else:
                print("未检测到有效封面，将等待60s重试")
            time.sleep(60)
            
    result = testword(new["标题"])
    for word in result:
        new["标题"] = new["标题"]。replace(word,mypinyin(word))
    result = testword(new["内容"])
    for word in result:
        new["内容"] = new["内容"]。replace(word,mypinyin(word))
    print('标题：'+new["标题"])
    print('正文：\n'+new["内容"]+'\n\n'+config("标签"))
    input()

if __name__ == '__main__': 
    main()
    input()

# ブラウザを自動操作するためseleniumをimport

from selenium import webdriver#import selenium
from selenium.webdriver.common.keys import Keys# seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.chrome.options import Options# seleniumでヘッドレスモードを指定するためにimport
import time# 待ち時間を指定するためにtimeをimport
import re# 正規表現にマッチする文字列を探すためにreをimport

# Googleのトップページ
URL= "https://www.google.com/?hl=ja"#Googleのトップページにいったら、タイトリに”Google”が含まれているか確認するために指定

def main():
    '''#コメントアウト
    メインの処理（関数化）
    Googleの検索エンジンでキーワードを検索
    指定されたドメインが検索結果の１ページ目に含まれていないキーワードをテキストファイルに出力
    '''#コメントアウト　→ドックストリング


    # '検索キーワードリスト.txt'ファイルを読み込み、リストにする
    with open("検索キーワードリスト.text", encoding="utf-8") as f:
        keywords = [s.rstrip() for s in f.readlines()]   #1行ずつ読み込んで改行コードを削除してリストにする
        ##.rstrip(除去する文字)、"s."":文字列
        # #    keywords =[s.rstrip() for in f.readlines()]#1行ずつ読み込んで改行コードそのままの状態でリストにする

    # 'ドメインリスト.txt'ファイルを読み込み、リストにする
    with open("ドメインリスト.txt", encoding="utf-8") as f:
        domains = [s.rstrip() for s in f.readlines()]   # １行ずつ読み込んで改行コードを削除してリストにする

    # seleniumで自動操作するブラウザはGoogleChrome

    # Optionsオブジェクトを作成
    options = Options()#Optionsオブジェクトの作成 #webdriver.ChromeOptions()
    options.add_argument('--headless')# ヘッドレスモードを有効にする#googleclomeを立ち上げない
    #.add_argument():()内のコマンドライン引数を指定する関数 #--headless:ヘッドレスモード（バックグラウンド）で起動# ChromeのWebDriverオブジェクトを作成
    driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\1170026\Desktop\udemy\00_デイトラ\pythonチュートリアル\chromedriver.exe")
    #C:\Users\1170026\Desktop\udemy\00_デイトラ\pythonチュートリアル
    ##exeファイルの実行、##rを忘れない！
    driver.get(URL)  # Googleのトップページを開く
    time.sleep(2)  # 2秒待機（読み込みのため）
    # タイトルに"Google"が含まれていることを確認
    ok_keywordlist = []
    for keyword in keywords:  # 検索キーワードを１つずつ取り出す
        search(keyword, driver)   # search関数実行
        urls = get_url(driver)  # get_url関数を実行し、戻り値をurlsに代入
        print(urls)
        weak_keywordlist = domain_checked(urls, domains, ok_keywordlist, keyword)  # domain_checked関数を実行し、戻り値をok_keywordlistに代入

    with open("結果.text", "w") as f:  # '結果.txt'という名前を付けて、ドメインチェックしたキーワードをファイルに書き込む("w")
        f.write("\n".join(weak_keywordlist))
        # ドメインチェック済みのキーワードを１行ずつ保存
    driver.quiet()  # ブラウザーを閉じる

def search(keyword,driver):
    '''
    検索テキストボックスに検索キーワードを入力し、検索する
    '''
    #参照urlは右記(通常で開くとnameが見つからない）：https://www.google.com/?hl=ja
    input_element = driver.find_element_by_name("q")  # 検索テキストボックスの要素をname属性から取得#検索ボックスの要素に変えて指定（name →他の要素）
    input_element.clear()  # 検索テキストボックスに入力されている文字列を消去
    input_element.send_keys(keyword)  # 検索テキストボックスにキーワードを入力
    input_element.send_keys(Keys.RETURN)  # Enterキーを送信
    time.sleep(2)  # 2秒待機

def get_url(driver):
    '''
    検索結果ページの1位から10位までのURLを取得
    '''
    urls = []# 各ページのURLを入れるためのリストを指定
    objects = driver.find_elements_by_css_selector(" div > a")  # a要素（各ページの1位から10位までのURL）取得
    #objects = driver.find_elements_by_css_selector("div.Z26q7c.UK95Uc.jGGQ5e > div > a")  # エラーのため対応
    #エラー対応　"div > a >"読み込まなかったため、範囲を拡大して検索"div.Z26q7c.UK95Uc.jGGQ5e > div > a"
    #by_css_selector:結果をリストとして返す
    ###rso > div:nth-child(1) > div > div > div.Z26q7c.UK95Uc.jGGQ5e > div > a
    # objects = driver.find_elements_by_css_selector('.rc > .r > a')
    if objects:
        for object in objects:
            urls.append(object.get_attribute("href"))  # 各ページのURLをリストに追加#a要素から、各ページのurlを取得、リストに追加
    else:
        print("URLが取得できませんでした")  # 各ページのURLが取得できなかった場合は警告を出す#各ページのURLが首都機できなかった場合は警告を出す
    return urls  # 各ページのURLを戻り値に指定

def domain_checked(urls, domains, ok_keywordlist, keyword):
    '''
    URLリストからドメインを取得し、指定ドメインに含まれているかチェック
    '''
    #ドメイン例http://abcd.com/ http://www.abcd.com/
    for url in urls:  # URLリストから各ページのURLを１つずつ取り出す
        #m = re.search(r'//(,*?)/', url)  # '//〇〇/'に一致する箇所（ドメイン）を抜き出す
        #domain =m.group(1)  # '//〇〇/'の'〇〇'に一致する箇所を抜き出し、domainに代入
        m = re.search(r'//(.*?)/', url)  # '//〇〇/'に一致する箇所（ドメイン）を抜き出す
        domain = m.group(1)  # '//〇〇/'の'〇〇'に一致する箇所を抜き出し、domainに代入
        if "www." in domain:  # ドメインに'www.'が含まれているかチェック
            domain = domain[4:]  # 含まれているなら'www.'を除去
        if domain in domains:  # 各ページのドメインが指定ドメインに含まれているかチェック
            print(f'キーワード「{keyword}」の検索結果には大手ドメインがありましたので除外します。')# 含まれているなら警告を出す
            break  # １つでも含まれているなら他はチェックする必要がないので関数を終了
        else:
            ok_keywordlist.append(keyword)  # 指定ドメインに含まれていないならキーワードをok_keywordlistに追加
    return ok_keywordlist  # ドメインチェック済みのキーワードを戻り値に指定


main()# main関数を実行
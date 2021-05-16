import pandas as pd
import datetime

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_order_count=[]
        self.item_master=item_master
    
    #オーダーを入力し、マスターに登録されているかをチェック、あればオーダー登録
    def add_item_order(self):
        while True:
            input_code = input("商品コードを入力してください / 終了時は「0」を入力してください＝＞")
            if input_code!="0":
                master_code_check=[]
                for master_code in self.item_master:
                    master_code_check.append(master_code.item_code)
                if input_code in master_code_check:
                    self.item_order_list.append(input_code)
                    input_count=input("個数を入力してください")
                    self.item_order_count.append(input_count)
                else:
                    print("入力された商品コードはありません")
            else:
                print("入力を終了します")
                break
    
    #商品コードからマスターに登録した商品名と価格を探す
    def item_search(self,item):
        for search in self.item_master:
            if item == search.item_code:
                return search.item_name,search.price

    #オーダー内容を表示する
    def view_item_list(self):
        self.total_price=0
        for item,count in zip(self.item_order_list,self.item_order_count):
            name_price=self.item_search(item)
            item_total_price=int(name_price[1])*int(count)
            self.write_receipt(f"商品コード:{item} 商品名:{name_price[0]} 価格:{name_price[1]}円 =>注文個数:{count}個 合計金額:{item_total_price}円")
            self.total_price+=item_total_price
        self.write_receipt(f"お買い上げの合計金額は{self.total_price}円になります")

    #お会計
    def calculation_change(self):
        while True:
            payment=int(input("支払い金額を入力してください=>"))
            if payment > self.total_price:
                change=payment-self.total_price
                self.write_receipt(f"{payment}円お預かりします。お釣り{change}円になります")
                print("ありがとうございました")
                time_now = datetime.datetime.now()
                write_time=time_now.strftime('%Y年%m月%d日 %H:%M:%S')
                self.write_receipt(write_time)
                break
            elif payment == self.total_price:
                self.write_receipt(f"{payment}円ちょうどお預かりします")
                print("ありがとうございました")
                time_now = datetime.datetime.now()
                write_time=time_now.strftime('%Y年%m月%d日 %H:%M:%S')
                self.write_receipt(write_time)
                break
            else:
                print("支払い金額が足りません。もう一度入力してください")
    
    def write_receipt(self,text):
        print(text)
        with open("レシート.txt", mode="a", encoding='UTF-8') as f:
            f.write(text+"\n")

            

        


#マスター登録
def master_input():
    master_list=[]
    df=pd.read_csv("master.csv",dtype=object)
    code_list=(list(df["商品コード"]))
    name_list=list(df["商品名"])
    price_list=list(df["価格"])
    for code,name,price in zip(code_list,name_list,price_list):
        master_list.append(Item(code,name,price))
    return master_list


    
    
### メイン処理
def main():
    # マスタ登録
    item_master=master_input()
    
    # オーダー登録
    order=Order(item_master)
    order.add_item_order()
   
    # オーダー表示
    order.view_item_list()

    #お会計
    order.calculation_change()
    
if __name__ == "__main__":
    main()
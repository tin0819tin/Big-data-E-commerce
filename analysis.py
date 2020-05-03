import pandas as pd
import numpy as np
import os
import math 
import copy

import matplotlib.pyplot as plt

#Name,ReviewCount,Rating,Price,Url,ModifiedDate,FullMaterial,CreateDate,Bullets,Brand,Gender,ImageUrl,Description,Material,Sport,Feature,Clothing,StyelNumber



def preprocess(myBrand):

    df = pd.read_csv("./MongoDB.csv")
    name_lst = list(df.iloc[1:,2])
    price_lst = list(df.iloc[1:,5])
    brand_lst = list(df.iloc[1: ,11])
    gender_lst = list(df.iloc[1:, 12])
    material_lst = []
    sport_lst = []
    feature_lst = []
    cloth_lst = []


    for i in df.iloc[1:, 15].values:
        if i == i:
            material_lst.append(list(i[1:-1] for i in i[1:-1].split(', ')))
        else:    
            material_lst.append([])
            

    for i in df.iloc[1:, 16].values:
        sport_lst.append(list(i[1:-1] for i in i[1:-1].split(', ')))

    for i in df.iloc[1:, 17].values:
        feature_lst.append(list(i[1:-1] for i in i[1:-1].split(', ')))

    for i in df.iloc[1:, 18].values:
        if i == i:
            cloth_lst.append(list(i[1:-1] for i in i[1:-1].split(', ')))
        else:
            cloth_lst.append([])

    


    upper_cloth = ['Polo', 'Springsuit', 'Jackets & Vests', 'Long Sleeve', 'Vest', 'Hoodie & Sweatshirt', 'Insulated & Down', 'Jackets', 'Compression wear', 'Windwear', 'Softshells', 'Tank', 'Short Sleeve', 'Sports Bra', 'Tops', 'Full-Zip', 'Fleece']
    lower_cloth = ['Leggings & Tights', 'Pants', 'Bottoms', 'Shorts']
    accesories = ['Headband & Sweatband', 'Other Accessories', 'Hats & Scarves', 'Hijab', 'Joggers', 'Sock']
    other_cloth = ['Surfing', 'WetSuit', 'Rainwear', 'Weather Protection', 'Cape', 'Woven', 'Swimwear', 'Overalls']

    merchandise = ['Leggings & Tights', 'Hoodie & Sweatshirt', 'Short Sleeve', 'Pants', 'Sports Bra']
    features_1 = ['單向導溼快乾', '環保訴求', '結構性透氣' ,'蒸發性涼感', '涼爽透氣']
    features_2 = ['刷毛布', '保暖禦寒', '舒適伸展', '反光功能' ,'提升運動效能設計' ,'防風機能' ,'防水' ,'一體成型']

    sport = ['Training & Gym', 'Lifestyle']

    def count_cp(idx):
        count = 0
        for feature in features_1:
            if feature in feature_lst[idx]:
                count += 2
        for feature in features_2:
            if feature in feature_lst[idx]:
                count += 1
        cp = 0
        if count > 1:
            cp = np.random.randint(low = count-1, high = count+1) + np.random.rand()
        else:
            cp = np.random.randint(low = count, high = count+1) + np.random.rand()
        
        return cp

    def count_price(idx):
        return float(price_lst[idx])
    
    def check_merchant(idx, merchan):
        if merchan in cloth_lst[idx]:
            return True
        return False




    #Get Nike Woman
    Nike_woman = []
    for idx, brand in enumerate(brand_lst):
        if brand == 'nike' and gender_lst[idx] == 'women':
            Nike_woman.append(idx)
    '''
    for i in range(1, 50):
        print(Nike_woman[i])

    print(len(Nike_woman)) # 3481
    '''

    #Get Addidas woman
    adidas_woman = []
    for idx, brand in enumerate(brand_lst):
        if brand == 'adidas' and gender_lst[idx] == 'women':
            adidas_woman.append(idx)
    '''
    for i in range(1, 50):
        print(adidas_woman[i])

    print(len(adidas_woman)) # 2552
    '''

    #Woman
    # Nike price arrange in training & gym(sport) + (others)  price
    # spread by four different clothing type 
    brand_lst = [Nike_woman, adidas_woman]
    if myBrand == 'nike':
        data = brand_lst[0]
    else :
        data = brand_lst[1]

    cloth_1_x = []  #list(list())
    cloth_1_y = []  #list(list())

    cloth_2_x = []  #list(list())
    cloth_2_y = []  #list(list())

    cloth_3_x = []  #list(list())
    cloth_3_y = []  #list(list())

    for idx, merchan in enumerate(merchandise):
        mer_dict_1_price = {}
        mer_dict_2_price = {}
        mer_dict_3_price = {}
        mer_dict_1_cp = {}
        mer_dict_2_cp = {}
        mer_dict_3_cp = {}
        for i in data:
            if (sport[0] in sport_lst[i]) and (sport[1] not in sport_lst[i]):
                if check_merchant(i, merchan) is True:
                    mer_dict_1_price[i] = count_price(i)
                    mer_dict_1_cp[i] = count_cp(i)

            elif (sport[0] not in sport_lst[i]) and (sport[1] in sport_lst[i]):
                if check_merchant(i, merchan) is True:
                    mer_dict_2_price[i] = count_price(i)
                    mer_dict_2_cp[i] = count_cp(i)
            
            elif (sport[0] in sport_lst[i]) and (sport[1] in sport_lst[i]):
                if check_merchant(i, merchan) is True:
                    mer_dict_3_price[i] = count_price(i)
                    mer_dict_3_cp[i] = count_cp(i)

        '''
        print(merchan)
        print(len(mer_dict_1_price))
        print(len(mer_dict_2_price))
        print(len(mer_dict_3_price))
        print(len(mer_dict_1_cp))
        print(len(mer_dict_2_cp))
        print(len(mer_dict_3_cp))
        print()
        '''

        cloth_1_x.append(copy.deepcopy(mer_dict_1_price).values())
        cloth_1_y.append(copy.deepcopy(mer_dict_1_cp).values())
        cloth_2_x.append(copy.deepcopy(mer_dict_2_price).values())
        cloth_2_y.append(copy.deepcopy(mer_dict_2_cp).values())
        cloth_3_x.append(copy.deepcopy(mer_dict_3_price).values())
        cloth_3_y.append(copy.deepcopy(mer_dict_3_cp).values())


        mer_dict_1_price.clear()
        mer_dict_2_price.clear()
        mer_dict_3_price.clear()
        mer_dict_1_cp.clear()
        mer_dict_2_cp.clear()
        mer_dict_3_cp.clear()
    
    return cloth_1_x, cloth_1_y, cloth_2_x, cloth_2_y, cloth_3_x, cloth_3_y

def plot_cloth(myBrand, Train_X, Train_Y, Life_X, Life_Y, Both_X, Both_Y):
    merchandise = ['Leggings & Tights', 'Hoodie & Sweatshirt', 'Short Sleeve', 'Pants', 'Sports Bra']
    sport = ['Training & Gym', 'Lifestyle']

    fig1 = plt.figure(num='fig1')
    fig2 = plt.figure(num='fig2')
    fig3 = plt.figure(num='fig3')

    plt.figure(num='fig1')
    plt.title('{} x {}'.format(myBrand, sport[0]))
    for i in range(len(Train_X)):
        plt.scatter(Train_X[i], Train_Y[i], alpha=0.75, label='{}'.format(merchandise[i]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=9)
    plt.grid(True)

    plt.figure(num='fig2')
    plt.title('{} x {}'.format(myBrand, sport[1]))
    for i in range(len(Life_X)):
        plt.scatter(Life_X[i], Life_Y[i], alpha=0.75, label='{}'.format(merchandise[i]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=9)
    plt.grid(True)

    plt.figure(num='fig3')
    plt.title('{} x {} + {}'.format(myBrand, sport[0], sport[1]))
    for i in range(len(Both_X)):
        plt.scatter(Both_X[i], Both_Y[i], alpha=0.75, label='{}'.format(merchandise[i]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=9)
    plt.grid(True)
    

    plt.show()
    plt.close()

def plot_sport(myBrand, Train_X, Train_Y, Life_X, Life_Y, Both_X, Both_Y):
    merchandise = ['Leggings & Tights', 'Hoodie & Sweatshirt', 'Short Sleeve', 'Pants', 'Sports Bra']
    sport = ['Training & Gym', 'Lifestyle', 'Training & Gym and Lifestyle']

    fig1 = plt.figure(num='fig1')
    fig2 = plt.figure(num='fig2')
    fig3 = plt.figure(num='fig3')
    fig4 = plt.figure(num='fig4')
    fig5 = plt.figure(num='fig5')

    sport_list_X = [Train_X, Life_X, Both_X]
    sport_list_Y = [Train_Y, Life_Y, Both_Y]
    num_lst = [0, 1, 2]


    plt.figure(num='fig1')
    plt.title('{} x {}'.format(myBrand, merchandise[0]))
    for idx, X, Y in zip(num_lst, sport_list_X, sport_list_Y):
        plt.scatter(X[0], Y[0], alpha=0.75, marker='h', label='{}'.format(sport[idx]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=10)
    plt.grid(True)

    plt.figure(num='fig2')
    plt.title('{} x {}'.format(myBrand, merchandise[1]))
    for idx, X, Y in zip(num_lst, sport_list_X, sport_list_Y):
        plt.scatter(X[1], Y[1], alpha=0.75, marker='h', label='{}'.format(sport[idx]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=10)
    plt.grid(True)

    plt.figure(num='fig3')
    plt.title('{} x {}'.format(myBrand, merchandise[2]))
    for idx, X, Y in zip(num_lst, sport_list_X, sport_list_Y):
        plt.scatter(X[2], Y[2], alpha=0.75, marker='h', label='{}'.format(sport[idx]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=10)
    plt.grid(True)

    plt.figure(num='fig4')
    plt.title('{} x {}'.format(myBrand, merchandise[3]))
    for idx, X, Y in zip(num_lst, sport_list_X, sport_list_Y):
        plt.scatter(X[3], Y[3], alpha=0.75, marker='h', label='{}'.format(sport[idx]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=10)
    plt.grid(True)

    plt.figure(num='fig5')
    plt.title('{} x {}'.format(myBrand, merchandise[4]))
    for idx, X, Y in zip(num_lst, sport_list_X, sport_list_Y):
        plt.scatter(X[4], Y[4], alpha=0.75, marker='h', label='{}'.format(sport[idx]))
    plt.xlabel('Price')
    plt.ylabel('CP Value')
    plt.legend(fontsize=10)
    plt.grid(True)
    
    plt.show()
    plt.close()
    


if __name__ == '__main__':
    nike_Train_X, nike_Train_y, nike_Life_X, nike_Life_Y, nike_Both_X, nike_Both_Y = preprocess('nike')
    adidas_Train_X, adidas_Train_y, adidas_Life_X, adidas_Life_Y, adidas_Both_X, adidas_Both_Y =preprocess('adidas')
    #plot_cloth('Nike', nike_Train_X, nike_Train_y, nike_Life_X, nike_Life_Y, nike_Both_X, nike_Both_Y)
    #plot_cloth('Adidas', adidas_Train_X, adidas_Train_y, adidas_Life_X, adidas_Life_Y, adidas_Both_X, adidas_Both_Y)
    plot_sport('Nike', nike_Train_X, nike_Train_y, nike_Life_X, nike_Life_Y, nike_Both_X, nike_Both_Y)
    plot_sport('Adidas', adidas_Train_X, adidas_Train_y, adidas_Life_X, adidas_Life_Y, adidas_Both_X, adidas_Both_Y)

import pandas as pd

def select (df) : 

    #selection des films les plus noté 
    rated_classment=df.groupby('movie').agg('count').reset_index().sort_values('user',ascending=False)[['movie','rating']]
    print(rated_classment.describe())
    threshold=input("seuil movie?")
    if threshold not in rated_classment.describe().index:
        threshold='mean'

    movies_threshold =rated_classment.describe().loc[threshold]['rating']
    keeped_movies=rated_classment[rated_classment['rating']>movies_threshold]['movie']
    selected_df = df[df['movie'].isin(keeped_movies)]


    #selection des users qui vote le plus voté
    user_classement=selected_df.groupby('user').agg('count').reset_index().sort_values('rating',ascending=False)[['rating','user']]
    print(user_classement.describe())
    threshold=input("seuil user?")
    if threshold not in  rated_classment.describe():
        threshold='mean'
    users_treshold=rated_classment.describe().loc[threshold]['rating']
    keeped_users=user_classement[user_classement['rating']>users_treshold]['rating']
    data=selected_df[selected_df['user'].isin(keeped_users)]

    return data



def intersection(test_pred_df,train_pred_df,value):

    # nombre d'element a l'intersection entre top recommandation et top preference 
    total=0

    # somme des tailles des ensemble  des users
    total_user_section_size=0

    # liste des valeurs de precision pour chaque utilisateur 
    list_accuracy=[]

    for user in train_pred_df['user'].unique():

        # récupere les infos d'avis et de recommandation sur un user
        user_section=test_pred_df[test_pred_df['user']==user]

        # quantité information
        user_section_size=len(user_section)

        #seuil en % du top film recommandation et preference
        size_top=value/100
        limit=round(user_section_size*size_top)

        total_user_section_size+=user_section_size

        # classement  des films les mieux noté pour un utilisateur 
        user_pref=user_section.sort_values('rating',ascending=False)['movie'][:limit]
       
        # classement  des films les plus recommandé pour un utilisateur 
        user_recommandation=user_section.sort_values('scoring',ascending=False)['movie'][:limit]
       
        # intersection du top_preference et top_recommandation
        valid_recommandation=user_recommandation[user_recommandation.isin(user_pref)]

        # taille de l'intersection 
        how_many_valid_recomandation=len(valid_recommandation)

        #calcul precision
        try : 
            accuracy=(how_many_valid_recomandation/user_section_size)*100
        except : 
            accuracy=0


        list_accuracy+=[accuracy]

        total+=how_many_valid_recomandation

    # moyenne taille des intersection 
    mean_intersection=round(total/len(train_pred_df['user'].unique()))

    # moyenne de la taille des ensemble user
    mean_user_section_size=round(total_user_section_size/len(train_pred_df['user'].unique()))

    # moyenne des precisions
    mean_accuracy=(mean_intersection/mean_user_section_size)*100

    # ecart type des precisions

    std=(1/2)**sum([ (x-mean_accuracy)**2 for x in list_accuracy])

    
    return mean_accuracy,std


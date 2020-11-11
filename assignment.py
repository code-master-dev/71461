try:
    import pandas as pd
except:
    print("Please install pandas")
    print(("open cmd and run command:: pip install pandas"))
try:
    import matplotlib.pyplot as plt
except:
    print("Please install matplotlib")
    print(("open cmd and run command:: pip install matplotlib"))
    input("Press enter to terminate...")

try:
    import urllib.request
    import bs4 as bs
    import urllib.request


    def state_dataframe():
        #links for web scrapping
        scrap_ar = [
        "https://www.crestcapital.com/tax/us_states_and_capitals",
        "https://statesymbolsusa.org/categories/flower",
        "https://worldpopulationreview.com/states/state-capitals/"
        ]
        # Creating the html source for the link "https://www.crestcapital.com/tax/us_states_and_capitals" to scrap
        source = urllib.request.urlopen(scrap_ar[0]).read()
        # Making a bs4 object
        soup = bs.BeautifulSoup(source,'lxml')
        capital_ar = []
        sub_arr = []
        #Getting the values in <div class="sub_text"> and creating a array of arrayes
        for div in soup.find_all('div', class_='sub_text'):
            for i in div.text.split('\n'):
                if len(i) > 0:
                    if ':' in i:
                        sub_arr.append(str(i.split(': ')[-1]).strip('\r'))
                    else:
                        sub_arr.append(str(i.strip('\r')).strip())
                
            capital_ar.append(sub_arr)
            sub_arr = []
        # Creating a df from capital_ar
        states_df = pd.DataFrame(capital_ar, columns=["State", "Capital", "State_Bird", "State_Flower"])
        # Dropping duplicates from the df
        states_df.drop_duplicates(subset=['State'], keep='first', inplace=False, ignore_index=False)
        
        # Scrapping another website "https://worldpopulationreview.com/states/state-capitals/" for populaton
        df_con_pop = pd.read_html(scrap_ar[2])[0]
        # Dropping unwanted columns
        df_con_pop.drop(columns=["Capital"], inplace=True)
        # Merging two datasets into one and naming it df 
        df = pd.merge(states_df, df_con_pop, on=['State'])
        df.drop_duplicates(subset=['State'], keep='first', inplace=True, ignore_index=False)
        df.drop(columns=['State_Bird'],inplace=True)
        #saving the dataset
        df.to_csv("StateData.csv", index=False)
        return df
    df = state_dataframe()
except:
    df = pd.read_csv('StateData.csv')
# Task 1
def show_complete_data(df):
    df.sort_values(by=['State'],inplace=True)
    print(df.to_string(index=False))

# Task 2
def show_image_and_data(df, state):
    print(pd.DataFrame(df.loc[df['State'] == state]).to_string(index=False))
    im_path = 'pic/'+str(list(df[df["State"] == state].State_Flower)[0])+'.jpg'
    img = plt.imread(im_path)
    plt.imshow(img)
    plt.show()

# Task 3
def top_five(df):
    top_5_df = df.sort_values(by=["State Population"], ascending=False)[:5]
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(list(top_5_df["State"]), list(top_5_df["State Population"]))
    plt.show()

#Task 4
def population_update(df, state, population):
    df.loc[list(df.loc[df['State'] == state].index)[0],'State Population'] = population
    print(f"Population updated for {state}.")

display = '''
1. Display all U.S. States in Alphabetical order along with the
Capital, State Population, and Flower
2. Search for a specific state and display the appropriate Capital
name, State Population, and an image of the associated State Flower.
3. Provide a Bar graph of the top 5 populated States showing their
overall population.
4. Update the overall state population for a specific state.
5. Exit the program
'''
run = True
while run:
    print(display)
    try:
        ip = int(input("Enter choice(Ex. 1)::"))
        assert(ip in [1, 2, 3, 4, 5])
        if ip == 1:
            show_complete_data(df)
        elif ip == 2:
            state = input("Enter the state name::")
            try:
                show_image_and_data(df, state=state)
            except:
                print("Enter correct data.")
        elif ip == 3:
            top_five(df)
        elif ip==4:
            try:
                state = input("Enetr the state name::")
                population = int(input("Enter updated population::"))
                population_update(df, state, population)
            except:
                print("Enter correct data.")
        else:
            #Task 5
            run = False
    except:
        pass
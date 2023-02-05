import pickle
def reset_data(nb):
    with open("data_"+str(nb)+".bin", "wb") as d:
        pickle.dump({"boards":[],"importance":[]},d)

reset_data(1)
reset_data(2)
reset_data(3)
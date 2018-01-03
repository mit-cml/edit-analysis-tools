import pickle

"""
    Proper use:
    You have some variable containing data you'd like to save for later, such as an array named "a": 
        a = bigComplicatedData
    To save this to disk:
        save_var(a, "a")
    In a future session, you can restore that data:
        a = restore_var("a")
"""


def save_var(variable, name):
    """Saves the value of variable to disk as with the given name."""
    with open(name + '.pickle', 'wb') as f:
        pickle.dump(variable, f)


def restore_var(name):
    """Loads the value saved in the pickle of the given name and returns that value."""
    print("Restoring " + name + " data...")
    with open(name + '.pickle', 'rb') as f:
        p = pickle.load(f)
    return p

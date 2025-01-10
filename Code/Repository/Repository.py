class Repository:
    def __init__(self, path, df):
        self.path = path
        self.df = df
        print("Creating repository at path: "+self.path)

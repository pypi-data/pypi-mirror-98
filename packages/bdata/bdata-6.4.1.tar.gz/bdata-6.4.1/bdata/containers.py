from mudpy.containers import mvar, mhist, mdict

class vdict(mdict):
    def set(self, key, **kwargs):
        self[key] = mvar(**kwargs)
        
class hdict(mdict):
    def set(self, key, **kwargs):
        self[key] = mhist(**kwargs)

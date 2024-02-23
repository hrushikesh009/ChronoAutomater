from selenium import webdriver


class LocalStorage:
    def __init__(self, driver: webdriver) :
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return localStorage.length;")
    
    def items(self) :
        local_storage_script = """
            var localStorageData = {};
            for (var i = 0; i < localStorage.length; i++) {
                var key = localStorage.key(i);
                var value = localStorage.getItem(key);
                localStorageData[key] = value;
            }
            return JSON.stringify(localStorageData);
        """
        return self.driver.execute_script(local_storage_script)

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = localStorage.length, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return localStorage.getItem(arguments[0]);", key)
    
    def set(self, key, value):
        self.driver.execute_script("localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("localStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()
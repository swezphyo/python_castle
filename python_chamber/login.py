class login:
    def __init__(self, id, pas):
        self.id = id
        self.pas = pas

    def check(self, id, pas):
        print self.id
        if self.id == id and self.pas == pas:
            print "Login success!"

log = login("admin", "admin")
log.check(raw_input("Enter Login ID:"),
          raw_input("Enter password: "))
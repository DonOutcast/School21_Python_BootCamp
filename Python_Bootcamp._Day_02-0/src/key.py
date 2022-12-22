class Key(object):
    passphrase = "zax2rulez"

    def __str__(self):
        return "GeneralTsoKeycard"

    def __len__(self):
        return 1337

    def __getitem__(self, item):
        return 3

    def __gt__(self, nbr):
        if nbr <= 9000:
            return 1
        else:
            return 0


key = Key()
assert len(key) == 1337
assert key[404] == 3
assert key > 9000
assert key.passphrase == "zax2rulez"
assert str(key) == "GeneralTsoKeycard"

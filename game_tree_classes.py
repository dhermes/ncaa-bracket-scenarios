import string


_BASE64_ALPHABET = (string.ascii_uppercase + string.ascii_lowercase +
                    string.digits + '+/')
BASE64_ALPHABET_DICT = {str(i + 1): letter
                        for i, letter in enumerate(_BASE64_ALPHABET)}
BASE64_ALPHABET_REVERSE = {letter: i
                           for i, letter in BASE64_ALPHABET_DICT.iteritems()}
KEY_SET = set(map(str, range(127)))


class GameSlots(object):

    def __init__(self, mapping=None):
        self.data = {} if mapping is None else mapping

    def copy(game_slots):
        return GameSlots(game_slots.data.copy())

    def add_slot(self, slot_id, obj):
        slot_id = str(int(slot_id))
        if slot_id in self.data:
            raise Exception('%s already claimed' % slot_id)

        self.data[slot_id] = obj

    def get_slot(self, slot_id):
        slot_id = str(int(slot_id))
        return self.data[slot_id]

    def reset_slot(self, slot_id, obj):
        slot_id = str(int(slot_id))
        if slot_id not in self.data:
            raise Exception('%s hasn\'t been claimed yet' % slot_id)

        self.data[slot_id] = obj

    @property
    def complete(self):
        assert set(self.data.keys()) == KEY_SET
        for value in self.data.itervalues():
            if not isinstance(value, Team):
                return False
        return True

    @property
    def reduced(self):
      if not self.complete:
          return super(Team, self).__hash__()
      else:
          # Since complete, we know keys == KEY_SET
          result_list = []
          for i in range(127):
              team = self.data[str(i)]
              result_list.append(BASE64_ALPHABET_DICT[team.team_id])
          return ''.join(result_list)

    @classmethod
    def from_reduced(cls, reduced):
        mapping = {}
        assert len(reduced) == 127
        for i in range(127):
            mapping[str(i)] = Team(BASE64_ALPHABET_REVERSE[reduced[i]])
        return cls(mapping=mapping)

    def __eq__(self, other):
        if not isinstance(other, GameSlots):
            return False
        if not (self.complete and other.complete):
            return False
        return self.reduced == other.reduced

    def __repr__(self):
        return 'GameSlots(slots=%s)' % self.data.keys()


class Team(object):

    def __init__(self, team_id):
        # Make sure it is an integer
        self.team_id = str(int(team_id))

    def __eq__(self, other):
        if not isinstance(other, Team):
            return False
        return self.team_id == other.team_id

    def __repr__(self):
        return 'Team(%s)' % self.team_id


class WinnerOf(object):

    def __init__(self, game_slot1, game_slot2):
        self.game_slot1 = game_slot1
        self.game_slot2 = game_slot2

    def __repr__(self):
        return 'WinnerOf(slot=%s, slot=%s)' % (self.game_slot1, self.game_slot2)

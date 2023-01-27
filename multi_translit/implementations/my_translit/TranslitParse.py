import json

from iso_tools.bcp47.make_preferred_form import make_preferred_form
from multi_translit.toolkit.py_ini import read_D_html_ini
from multi_translit.implementations.my_translit.get_rule import get_rule, process_val


next_fn = next


class TranslitParse:
    def __init__(self, path, direction='=>'):
        self.direction = direction

        D = read_D_html_ini(path)
        DConfig = self.DConfig = json.loads(self.remove_comments(D['settings']))
        self.DVariables = self.get_variables_dict(self.remove_comments(D.get('variables', '')))

        # HACK HACK HACK!
        DConfig['from_iso'] = make_preferred_form(DConfig['from_iso'])
        DConfig['to_iso'] = make_preferred_form(DConfig['to_iso'])

        # Get case-related properties
        self.ignore_case = DConfig.get('ignore_case', False)
        self.match_case = DConfig.get('match_case', False)

        self.from_iso = (DConfig['from_iso'] if direction == '=>' else DConfig['to_iso'])
        self.to_iso = (DConfig['to_iso'] if direction == '=>' else DConfig['from_iso'])

        self.LRules = [
            get_rule(
                self.replace_variables(rule.strip()),
                reverse=direction == '<=',
                ci_conditions=self.ignore_case or self.match_case
            )
            for rule in self.remove_comments(D['conversions']).split('\n')
        ]

        # Do various checks
        assert direction in ('=>', '<=')
        assert not (DConfig.get('direction') == '=>' and direction == '<=')
        assert not (DConfig.get('direction') == '<=' and direction == '=>')
        assert not DConfig.get('ignore_me'), "I've been ignored!"

        # Get the modifiers to use
        DModifiers = (
            DConfig.get('modifiers', {})
                   .get('from_direction' if direction == '=>' else 'to_direction', {})
        )
        self.LFromModifiers = DModifiers.get('before_conversions', {})
        self.LToModifiers = DModifiers.get('after_conversions', {})

        self.DRules = self.get_rules_dict()

        # Clean up
        del self.LRules
        del self.DVariables

    def get_rules_dict(self):
        D = {}
        for rule in self.LRules:
            from_side = rule.from_side

            for k in ('LSelf', 'LInitial', 'LMedial', 'LFinal'):
                L = getattr(from_side.conversions, k)
                if not L:
                    continue

                for s in L:
                    if not s:
                        continue

                    next_D = D
                    cur_L = None

                    for c in s:
                        if self.ignore_case or self.match_case:
                            c = c.lower()
                        next_D, cur_L = next_D.setdefault(c, ({}, []))

                    cur_L.append((k, rule.from_side, rule.to_side))
        return D

    def match(self, converted, before, next):
        if self.ignore_case or self.match_case:
            # TODO: Don't do this every time to increase performance(!)
            converted = converted.lower()
            before = before.lower()
            next = next.lower()

        next_D = self.DRules
        len_next = len(next)

        LTry = []
        for x, c in enumerate(next):
            if not c in next_D:
                break

            next_D, i_L = next_D[c]
            if i_L:
                LTry.append((x, i_L))

        for x, i_L in reversed(LTry):
            for k, from_side, to_side in i_L:
                if k == 'LSelf' and (before or len_next-1 != x):
                    continue
                elif k == 'LInitial' and (before or len_next-1 == x):
                    continue
                elif k == 'LMedial' and (not before or len_next-1 == x):
                    continue
                elif k == 'LFinal' and (not before or len_next-1 != x):
                    continue

                cond = from_side.conditions
                if cond.LBefore:
                    found = False
                    for t2 in cond.LBefore:
                        if next.startswith(t2, x+1):
                            found = True
                            break

                    if not found:
                        continue

                if cond.LAfter:
                    found = False
                    for t2 in cond.LAfter:
                        if before.endswith(t2):
                            found = True
                            break

                    if not found:
                        continue

                if to_side.conditions.LAfter:
                    found = False
                    for t2 in to_side.conditions.LAfter:
                        if converted.endswith(t2):
                            found = True
                            break

                    if not found:
                        continue

                conv_to = (
                    getattr(to_side.conversions, k) or
                    next_fn(i for i in to_side.conversions if i)
                )[0] # WARNING!
                #print conv_to, to_side.conversions, from_side.conversions
                return x+1, conv_to

        return None

    def get_variables_dict(self, s):
        D = {}
        for line in s.split('\n'):
            #print line.encode('utf-8')
            if not line:
                continue
            k, v = line.split(' = ')

            for i_k, i_v in list(D.items()):
                v = v.replace('$%s' % i_k, i_v)

            D[k.strip()] = process_val(v.strip())
        return D

    def replace_variables(self, s):
        for i_k, i_v in sorted(list(self.DVariables.items()),
                               key=lambda x: -len(x[0])):
            s = s.replace('$%s' % i_k, i_v)
        return s

    def remove_comments(self, s):
        return '\n'.join([i for i in s.split('\n')
                          if not i.startswith('#') and i.strip()])

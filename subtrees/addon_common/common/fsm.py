'''
Copyright (C) 2018 CG Cookie
https://github.com/CGCookie/retopoflow
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from ..common.debug import debugger
from ..common.utils import find_fns


def get_state(state, substate):
    return '%s__%s' % (str(state), str(substate))

class FSM:
    def __init__(self):
        self.wrapper = self._create_wrapper()

    def _create_wrapper(self):
        fsm = self
        class FSM_State:
            def __init__(self, state, substate='main'):
                self.state = state
                self.substate = substate

            def __call__(self, fn):
                self.fn = fn
                self.fnname = fn.__name__
                def run(*args, **kwargs):
                    try:
                        return fn(*args, **kwargs)
                    except Exception as e:
                        print('Caught exception in function "%s" ("%s", "%s")' % (
                            self.fnname, self.state, self.substate
                        ))
                        debugger.print_exception()
                        return
                run.fnname = self.fnname
                run.fsmstate = self.state
                run.fsmstate_full = get_state(self.state, self.substate)
                # print('%s: registered %s as %s' % (str(fsm), self.fnname, run.fsmstate_full))
                return run
        return FSM_State

    def init(self, obj, start='main'):
        self._obj = obj
        self._state_next = start
        self._state = None
        self._fsm_states = {}
        self._fsm_states_handled = set()
        for (st,fn) in find_fns(self._obj, 'fsmstate'):
            self._fsm_states_handled.add(st)
        for (m,fn) in find_fns(self._obj, 'fsmstate_full'):
            assert m not in self._fsm_states, 'Duplicate states registered!'
            self._fsm_states[m] = fn
            # print('%s: found fn %s as %s' % (str(self), str(fn), m))

    def _call(self, state, substate='main', fail_if_not_exist=False):
        s = get_state(state, substate)
        if s not in self._fsm_states:
            assert not fail_if_not_exist, 'Could not find state "%s" with substate "%s" (%s)' % (state, substate, str(s))
            return
        try:
            return self._fsm_states[s](self._obj)
        except Exception as e:
            print('Caught exception in state ("%s")' % (s))
            debugger.print_exception()
            return

    def update(self):
        if self._state_next is not None and self._state_next != self._state:
            if self._call(self._state, substate='can exit') == False:
                # print('Cannot exit %s' % str(self._state))
                self._state_next = None
                return
            if self._call(self._state_next, substate='can enter') == False:
                # print('Cannot enter %s' % str(self._state_next))
                self._state_next = None
                return
            # print('%s -> %s' % (str(self._state), str(self._state_next)))
            self._call(self._state, substate='exit')
            self._state = self._state_next
            self._call(self._state, substate='enter')
        ret = self._call(self._state, fail_if_not_exist=True)
        if ret is None:
            self._state_next = ret
            ret = None
        elif type(ret) is str:
            if ret in self._fsm_states_handled:
                self._state_next = ret
                ret = None
            else:
                self._state_next = None
                ret = ret
        elif type(ret) is tuple:
            st = {s for s in ret if s in self._fsm_states_handled}
            if len(st) == 0:
                self._state_next = None
                ret = ret
            elif len(st) == 1:
                self._state_next = next(st)
                ret = ret - st
            else:
                assert False, 'unhandled FSM return value "%s"' % str(ret)
        else:
            assert False, 'unhandled FSM return value "%s"' % str(ret)
        return ret

    @property
    def state(self):
        return self._state

    def force_set_state(self, state, call_exit=False, call_enter=True):
        if call_exit: self._call(self._state, substate='exit')
        self._state = state
        if call_enter: self._call(self._state, substate='enter')


def FSMClass(cls):
    cls.fsm = FSM()
    cls.FSM_State = cls.fsm.wrapper
    return cls

    # https://krzysztofzuraw.com/blog/2016/python-class-decorators.html
    # class Wrapper(object):
    #     def __init__(self, *args, **kwargs):
    #         self._wrapped = cls(*args, **kwargs)

